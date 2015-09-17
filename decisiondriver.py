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
utokens = tree.tokenizetweets(trainingu)
ctokens = tree.tokenizetweets(trainingc)
mtokens = tree.tokenizetweets(trainingm)
