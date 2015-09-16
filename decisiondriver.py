#the entry point for running decision tree code

import pickle
import operator

from utility.entropy import entropy
from decisiontree.decisiontree import DecisionTree

tree = DecisionTree()

ctweets = None
utweets = None
mtweets = None

with open('ctweets', 'rb') as c, open('utweets', 'rb') as u, open('mtweets', 'rb') as m:
    ctweets = pickle.load(c)
    utweets = pickle.load(u)
    mtweets = pickle.load(m)

utokens = {}
for key in utweets:
    tokens = tree.tokenizetweets(utweets[key])
    for t in tokens:
        utokens[t] = utokens.get(t, 0) + tokens[t]

sorted_utokens = sorted(utokens.items(), key=operator.itemgetter(1))

print (sorted_utokens)
