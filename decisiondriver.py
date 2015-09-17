#the entry point for running decision tree code

import pickle
import operator
import random

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

#Stripe tweets for testing
trainingc = []
testc = []

trainingu = []
testu = []

trainingm = []
testm = []

random.seed(123412)
for key in utweets:
  tweets = utweets[key]
  for t in tweets:
    if random.randrange(1,101) <= 90:
      trainingu.append(t)
    else:
      testu.append(t)
for key in ctweets:
  tweets = ctweets[key]
  for t in tweets:
    if random.randrange(1,101) <= 90:
      trainingc.append(t)
    else:
      testc.append(t)
for key in mtweets:
  tweets = mtweets[key]
  for t in tweets:
    if random.randrange(1,101) <= 90:
      trainingm.append(t)
    else:
      testm.append(t)

#create dictionaries of tokens
utokens = tree.tokenizetweets(trainingu).items()
ctokens = tree.tokenizetweets(trainingc).items()
mtokens = tree.tokenizetweets(trainingm).items()

utokens = sorted(utokens, key=operator.itemgetter(1), reverse=True)
ctokens = sorted(ctokens, key=operator.itemgetter(1), reverse=True)
mtokens = sorted(mtokens, key=operator.itemgetter(1), reverse=True)

#throw out all but the top 100 entries
utokens = utokens[0:100]
ctokens = ctokens[0:100]
mtokens = mtokens[0:100]

#gather all words
uwords = []
cwords = []
mwords = []

for t in utokens:
  uwords.append(t[0])
for t in ctokens:
  cwords.append(t[0])
for t in mwords:
  mwords.append(t[0])

#remove similar words
ucwords = list(set(uwords) | set(cwords))
umwords = list(set(uwords) | set(mwords))
cmwords = list(set(cwords) | set(mwords))

print (uwords)
print ('----')
print (cwords)
print ('----')
print (ucwords)
