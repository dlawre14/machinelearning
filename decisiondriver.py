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

#TODO: Stripe tweets for testing

utokens = {}
for key in utweets:
    tokens = tree.tokenizetweets(utweets[key])
    for t in tokens:
        utokens[t] = utokens.get(t, 0) + tokens[t]

ctokens = {}
for key in ctweets:
    tokens = tree.tokenizetweets(ctweets[key])
    for t in tokens:
        ctokens[t] = ctokens.get(t,0) + tokens[t]

mtokens = {}
for key in mtweets:
    tokens = tree.tokenizetweets(mtweets[key])
    for t in tokens:
        mtokens[t] = mtokens.get(t,0) + tokens[t]


sorted_utokens = sorted(utokens.items(), key=operator.itemgetter(1))
sorted_ctokens = sorted(ctokens.items(), key=operator.itemgetter(1))
sorted_mtokens = sorted(mtokens.items(), key=operator.itemgetter(1))

tree.tokencleaner(sorted_utokens, nourl = True)

print ('---')
print (sorted_utokens)
print ('---')
