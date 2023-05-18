import os
import glob
import re
import numpy as np
from gensim import corpora
from gensim.models import FastText
from gensim.models.callbacks import CallbackAny2Vec
from matplotlib import pyplot as plt
from tqdm import tqdm

class callback(CallbackAny2Vec):
    '''Callback to print loss after each epoch.'''

    def __init__(self):
        self.tq = tqdm(range(EPOCHS))
        self.progress = iter(self.tq)

    def on_epoch_end(self, model):
        loss = 4-model.wv.similarity('στρατιαν', 'δουλων')-model.wv.similarity('γνωσεως', 'καταβας')+model.wv.similarity('Χριστου', 'Ιησου')+model.wv.similarity('Θεος', 'αγαπη')
        self.tq.set_description(f'benchmark (larger better): {loss}')
        self.epoch = next(self.progress)
        losses[self.epoch] = loss

SIZE = 100
EPOCHS = 800

losses = np.zeros((EPOCHS,))

corpus = []

for fname in glob.glob('processed/*/*.txt'):
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.split('\n')
    text = [[word for word in line.split() if word.lower() != 'και'.lower()] for line in text]
    corpus += text

model = FastText(corpus, vector_size=SIZE, window=5, alpha=0.0005, negative=2, workers=16, epochs=EPOCHS, sg=1, min_count=4, callbacks=[callback()])
del model.callbacks
model.save(f'greek-fasttext-{SIZE}.bin')

plt.plot(losses)
plt.show()



