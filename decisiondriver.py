#the entry point for running decision tree code

import pickle
import operator
import random

from utility.entropy import entropy
from decisiontree.decisiontree import DecisionTree

import sys

sys.setrecursionlimit(3500) #might be dangerous

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

keyset = set()

for key in utokens:
  keyset.add(key)
for key in ctokens:
  keyset.add(key)
for key in mtokens:
  keyset.add(key)

entkeyvals = []
for key in keyset:
  ucount = utokens.get(key, 0)
  ccount = ctokens.get(key, 0)
  mcount = mtokens.get(key, 0)

  #classify as max
  classify = ''
  if ucount >= ccount and ucount >= mcount:
    classify = 'u'
  if ccount >= ucount and ccount >= mcount:
    classify = 'c'
  if mcount >= ucount and mcount >= ccount:
    classify = 'm'

  total = ucount + ccount + mcount

  #calculate probabilities
  ucount = ucount/total
  ccount = ccount/total
  mcount = mcount/total

  ent = entropy([ucount, ccount, mcount])

  entkeyvals.append((key, classify, ent))

entkeyvals = [x for x in entkeyvals if x[2] > 0]
entkeyvals = sorted(entkeyvals, key=operator.itemgetter(2))
entkeyvals.reverse()

tree.buildTree(tree.root, entkeyvals)

correct = 0
for tweet in testu:
  if tree.classify(tweet) == 'u':
    correct += 1

print ('Total u: ' + str(len(testu)) + ' Correct: ' + str(correct))
