from lemmatize import lemmatize_word
from gensim.models import Word2Vec
from random import choice

model = Word2Vec.load("greek-lemma-128.kv").wv

words = list(model.index_to_key)

def is_valid_choice(secret_word):
    "for now, check that secret word has top 1000 simillar words above similarity threshold"
    global top1K
    top1K = model.most_similar(secret_word, topn=1000)
    return top1K[-1][1] > 0.23

while True:
    secret_word = choice(words)
    if (not is_valid_choice(secret_word)):
        continue
    top1Kwords = [v[0] for v in top1K]
    isGuessed = False
    while not isGuessed:
        word = input()
        if not word:
            print('please enter a word\n')
            continue
        try:
            new_word = lemmatize_word(word)
            print('filtered guess:', new_word)
            if new_word in top1Kwords:
                print(new_word, 'is in top 1000 at', top1Kwords.index(new_word), '/ 1000')
            similarity = model.similarity(new_word, secret_word)
            print(f'similarity = {similarity*100:.2f}\n\n', end='')
            isGuessed = new_word == secret_word
        except KeyError:
            print('Word not found in dataset\n')
    print('you guessed it!\n\n')
