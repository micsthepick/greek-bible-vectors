from gensim.models import Word2Vec
import sys

SIZE = 100
if len(sys.argv) == 2:
    try:
        SIZE = int(sys.argv[1])
    except ValueError:
        pass

model = Word2Vec.load(f'greek-{SIZE}.kv').wv

get_sim = model.most_similar

import code
code.interact(local=dict(globals(), **locals()))
