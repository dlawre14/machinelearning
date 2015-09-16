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

uxx00tokens = tree.tokenizetweets(utweets['xx00'])
sorted_uxx00tokens = sorted(uxx00tokens.items(), key=operator.itemgetter(1))

print ('---')
print (sorted_uxx00tokens)
print ('---')
print (len(uxx00tokens.keys()))
