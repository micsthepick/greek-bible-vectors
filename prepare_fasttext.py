import os
import glob
import re
import numpy as np
from gensim.models import FastText
from gensim.models.callbacks import CallbackAny2Vec
from matplotlib import pyplot as plt
from tqdm import tqdm

class callback(CallbackAny2Vec):
    '''Callback to print loss after each epoch.'''

    def __init__(self):
        self.tq = tqdm(range(EPOCHS))
        self.progress = iter(self.tq)
        self.last_loss = 0.0

    def on_epoch_end(self, model):
        loss = 3-model.similarity('Χριστου', 'Ιησου')-model.similarity('Θεος', 'αγαπη')-model.similarity('Ιησου', 'αγαπη')
        #this_loss = loss - self.last_loss
        # self.last_loss = loss
        self.tq.set_description(f'benchmark: {this_loss}')
        self.epoch = next(self.progress)
        losses[self.epoch] = this_loss

SIZE = 100
EPOCHS = 2000

losses = np.zeros((EPOCHS,))

corpus = []

for fname in glob.glob('processed/*/*.txt'):
    print(fname)
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.split('\n')
    text = [[word for word in line.split() if word.lower() != 'και'.lower()] for line in text]
    corpus += text

model = FastText(vector_size=SIZE, workers=16, sg=1, min_count=2, callbacks=[callback()])
model.build_vocab(corpus_iterable=corpus)
model.train(corpus_iterable=corpus, total_examples=len(corpus), epochs=EPOCHS)
model.save(f'greek-fasttext-{SIZE}.bin')

#plt.plot(losses)
#plt.show()



