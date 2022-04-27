import os
import glob
import re
import numpy as np
from gensim import corpora
from gensim.models import Word2Vec
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
        loss = model.get_latest_training_loss()
        this_loss = loss - self.last_loss
        self.last_loss = loss
        self.tq.set_description(f'Loss: {this_loss:.3E}')
        self.epoch = next(self.progress)
        losses[self.epoch] = this_loss

SIZE = 100
EPOCHS = 400

losses = np.zeros((EPOCHS,))

corpus = []

for fname in glob.glob('processed/*/*.txt'):
    print(fname)
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.split('\n')
    text = [[word for word in line.split() if word.lower() != 'και'.lower()] for line in text]
    corpus += text

model = Word2Vec(corpus, vector_size=SIZE, workers=16, epochs=EPOCHS, sg=0, alpha=0.1, compute_loss=True, callbacks=[callback()])
model.save(f'greek-{SIZE}.kv')

plt.plot(losses)
plt.show()



