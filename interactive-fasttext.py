from gensim.models import FastText
import sys
import unicodedata as ud


SIZE = 100
if len(sys.argv) == 2:
    try:
        SIZE = int(sys.argv[1])
    except ValueError:
        pass

model = FastText.load(f'greek-fasttext-{SIZE}.bin').wv

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
    return ud.normalize('NFD',word).translate(d)

def get_sim(word):
    new_word = remove_diacritics(word)
    print(f'Getting words similar to {new_word}.')
    return model.most_similar(new_word)

import code
code.interact(local=dict(globals(), **locals()))
