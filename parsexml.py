import os
import xml.etree.ElementTree as ET

for d in os.listdir('xmldata'):
    dn = os.path.splitext(d)[0]
    tree = ET.parse('xmldata/'+d)
    root = tree.getroot()
    books = root[1:]
    if not os.path.isdir(f'processed/{dn}/'):
        os.makedirs(f'processed/{dn}/')
    for book in books:
        with open(f'processed/{dn}/{book.attrib["bname"]}.txt', 'w', encoding='utf-8') as f:
            for chapter in book:
                for verse in chapter:
                    if len(verse) > 0:
                        for word in verse:
                            print(word.text, file=f, end='')
                    else:
                        print(verse.text, file=f, end='')
                    print(file=f)
