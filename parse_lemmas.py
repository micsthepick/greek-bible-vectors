import os
import json
import xml.etree.ElementTree as ET
from unicodedata import normalize

DICTIONARY = set()

codes = [
    0x0060,
    0x0300,
    0x00A8,
    0x0308,
    0x00B4,
    0x0301,
    0x02BC,
    0x0313,
    0x02BD,
    0x0314,
    0x037A,
    0x0345,
    0x0384,
    0x0301,
    0x0385,
    0x0308,
    0x0301,
    0x1FBD,
    0x0313,
    0x1FBE,
#    0x03B9, # Iota
    0x1FBF,
    0x0313,
    0x1FC0,
    0x0342,
    0x1FC1,
    0x0308,
    0x0342,
    0x1FCD,
    0x0313,
    0x0300,
    0x1FCE,
    0x0313,
    0x0301,
    0x1FCF,
    0x0313,
    0x0342,
    0x1FDD,
    0x0314,
    0x0300,
    0x1FDE,
    0x0314,
    0x0301,
    0x1FDF,
    0x0314,
    0x0342,
    0x1FED,
    0x0308,
    0x0300,
    0x1FEE,
    0x0308,
    0x0301,
    0x1FEF,
    0x0300,
    0x1FFD,
    0x0301,
    0x1FFE,
    0x0314
]
# from http://opoudjis.net/unicode/gkdiacritics.html

d = {c:None for c in codes}

def remove_diacritics(word):
    return normalize('NFD',word).translate(d)


def normalize_greek(word):
    return normalize('NFC', remove_diacritics(word))

def process_js_file(input_path, output_dir):
    with open(input_path, 'rb') as file:
        byte_content = file.read()

    # Check for BOM
    if byte_content.startswith(b'\xef\xbb\xbf'):
        content_str = byte_content.decode('utf-8-sig')
    else:
        content_str = byte_content.decode('utf-8')

    content = json.loads(content_str)
    lemmas = []
    for key in content:
        for entry in content[key]:
            DICTIONARY.add(normalize_greek(entry['lemma']))

    lemmas = [' '.join([normalize_greek(entry['lemma']) for entry in content[key]]) for key in content]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, os.path.basename(input_path).replace('.js', '.txt'))
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lemmas))

def process_directory(input_dir, output_dir='./processed_lemma/OT'):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.js'):
                input_path = os.path.join(root, file)
                process_js_file(input_path, output_dir)


input_dir = 'GreekResources/LxxLemmas/'
process_directory(input_dir)
with open('GreekResources/GreekWordList.js', 'rb') as file:
    content_str = file.read().decode('utf-8-sig')

# Remove the comment block and the "greekWordList =" prefix
content_str = content_str.split('greekWordList =', 1)[-1].strip().strip(';')

try:
    lemma_key = json.loads(content_str)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON after modifications: {e}")


#lemma_key = {normalize_greek(key): value['lemma'] if 'lemma' in value else key for key, value in lemma_key.items()}
#new_dict = {}
strongsLemm = {}

for key, value in lemma_key.items():
    if "strong" in value:
        strongsLemm[value["strong"]] = normalize_greek(value["lemma"]) if "lemma" in value else key
    ### Add the lemma to map to itself
    ##lemma = key
    if "lemma" in value:
        DICTIONARY.add(normalize_greek(value["lemma"]))
        ##value["lemma"]
    ##else:
    ##    DICTIONARY.add(normalize_greek(key))
    ##new_dict[key] = lemma
    ### Extract derivatives and add them to the new dictionary
    ##if "deriv" in value:
    ##    for deriv in value["deriv"].split(','):
    ##        new_dict[normalize_greek(deriv.strip())] = lemma
    ##if "lemma" not in value and "deriv" not in value:
    ##    print(value)



def parsedirxml(d):
    dn = os.path.splitext(d)[0]
    tree = ET.parse('xmldata/'+d)
    root = tree.getroot()
    books = root[1:]
    numbers = {}

    if not os.path.isdir(f'processed_lemma/{dn}/'):
        os.makedirs(f'processed_lemma/{dn}/')
    #for book in books:
    #    for chapter in book:
    #        for verse in chapter:
    #            for word in verse:
    #                key = normalize_greek(word.text.strip())
    #                if (key in DICTIONARY):
    #                    strongs = word.get("str")
    #                    if (strongs in numbers and numbers[strongs] != key):
    #                        print(numbers[strongs], key)
    #                    numbers[strongs] = key
    for book in books:
        with open(f'processed_lemma/{dn}/{book.attrib["bname"]}.txt', 'w', encoding='utf-8') as f:
            for chapter in book:
                for verse in chapter:
                    for word in verse:
                        strongs = word.get("str")
                        if (strongs in strongsLemm):
                            print(strongsLemm[strongs], file=f, end=" ")
                            continue
                        print(strongs, word.text)
                    print(file=f)
parsedirxml('NT.xml')

