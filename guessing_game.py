from gensim.models import Word2Vec
from random import choice

model = Word2Vec.load('greek-100.kv').wv

words = list(model.index_to_key)

def is_valid_choice(word):
    # maybe do some checks...
    # default is a valid choice
    return True

while True:
    secret_word = choice(words)
    if not is_valid_choice(secret_word):
        continue
    isGuessed = 0
    while not isGuessed:
        word = input()
        try:
            similarity = model.similarity(word, secret_word)
            print(f'similarity = {similarity*100:.2f}\n\n', end='')
            isGuessed = similarity = 1
        except KeyError:
            print('Word not found in dataset (did you remove diacritics?)')
