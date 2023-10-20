import os
import json
import xml.etree.ElementTree as ET
from unicodedata import normalize

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

def lemmatize_word(word):
    word = normalize_greek(word)
    try:
        return lemmas[word]
    except KeyError:
        pass
    try:
        return strongsLemm[NT_lookup[word]]
    except KeyError:
        pass
    return word

with open('GreekResources/GreekWordList.js', 'rb') as file:
    content_str = file.read().decode('utf-8-sig')

# Remove the comment block and the "greekWordList =" prefix
content_str = content_str.split('greekWordList =', 1)[-1].strip().strip(';')

try:
    lemma_key = json.loads(content_str)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON after modifications: {e}")


strongsLemm = {}
lemmas = {}
NT_lookup = {}

for key, value in lemma_key.items():
    if "strong" in value:
        strongsLemm[value["strong"]] = normalize_greek(value["lemma"]) if "lemma" in value else key
    if "lemma" in value:
        lemmas[normalize_greek(key)] = normalize_greek(key)

def process_js_file(input_path):
    with open(input_path, 'rb') as file:
        byte_content = file.read()

    # Check for BOM
    if byte_content.startswith(b'\xef\xbb\xbf'):
        content_str = byte_content.decode('utf-8-sig')
    else:
        content_str = byte_content.decode('utf-8')

    content = json.loads(content_str)
    for key in content:
        for entry in content[key]:
            lemmas[normalize_greek(entry['key'])] = normalize_greek(entry['lemma'])

def parsedirxml(d):
    tree = ET.parse('xmldata/'+d)
    root = tree.getroot()
    books = root[1:]
    numbers = {}

    for book in books:
        for chapter in book:
            for verse in chapter:
                for word in verse:
                    strongs = word.get("str")
                    NT_lookup[normalize_greek(word.text.strip())] = strongs
parsedirxml('NT.xml')
