from gensim.models import Word2Vec
from random import choice
import unicodedata as ud

model = Word2Vec.load('greek-100.kv').wv

words = list(model.index_to_key)

def is_valid_choice(word):
    # maybe do some checks...
    # default is a valid choice
    return True

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
    0x03B9,
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

d = {c:None for c in codes}

while True:
    secret_word = choice(words)
    if not is_valid_choice(secret_word):
        continue
    isGuessed = 0
    while not isGuessed:
        word = input()
        try:
            new_word = ud.normalize('NFD',word).translate(d)
            print('filtered guess:', new_word)
            similarity = model.similarity(new_word, secret_word)
            print(f'similarity = {similarity*100:.2f}\n\n', end='')
            isGuessed = similarity = 1
        except KeyError:
            print('Word not found in dataset\n')
