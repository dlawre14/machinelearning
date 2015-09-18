#the entry point for running decision tree code

import pickle
import operator
import random

from utility.entropy import entropy
from decisiontree.decisiontree import DecisionTree

import sys

#sys.setrecursionlimit(1500) #might be dangerous

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

#strip out twitter handles
utokens = [x for x in utokens if '@' not in x[0]][0:300]
ctokens = [x for x in ctokens if '@' not in x[0]][0:300]
mtokens = [x for x in mtokens if '@' not in x[0]][0:300]

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

#remove duplciates
uc = list(set(uwords) & set(cwords))
um = list(set(uwords) & set(mwords))
cm = list(set(uwords) & set(mwords))

for word in uc:
  uwords.remove(word)
  cwords.remove(word)
for word in um:
  uwords.remove(word)
  mwords.remove(word)
for word in cm:
  cwords.remove(word)
  mwords.remove(word)

for i in range(len(utokens)):
  if utokens[i][0] not in uwords:
    utokens[i] = 'DELETE'

for i in range(len(ctokens)):
  if ctokens[i][0] not in cwords:
    ctokens[i] = 'DELETE'

for i in range(len(mtokens)):
  if mtokens[i][0] not in mwords:
    mtokens[i] = 'DELETE'

utokens = [x for x in utokens if x != 'DELETE']
ctokens = [x for x in ctokens if x != 'DELETE']
mtokens = [x for x in mtokens if x != 'DELETE']

wordtotal = 0

for x,y in utokens:
  wordtotal += y
for x,y in ctokens:
  wordtotal += y
for x,y in mtokens:
  wordtotal += y

for i in range(len(utokens)):
  utokens[i] = (utokens[i][0], utokens[i][1]/wordtotal)
for i in range(len(ctokens)):
  ctokens[i] = (ctokens[i][0], ctokens[i][1]/wordtotal)
for i in range(len(mtokens)):
  mtokens[i] = (mtokens[i][0], mtokens[i][1]/wordtotal)

tree.buildTree(entropy, None, utokens, ctokens, mtokens)

total=0
score=0
for tweet in testu:
    if tree.classify(tweet) == 'u':
        score += 1
    total+=1

print ('u score: ' + str(score/total))

total=0
score=0
for tweet in testc:
    if tree.classify(tweet) == 'c':
        score += 1
    total+=1

print ('c score: ' + str(score/total))

total=0
score=0
for tweet in testm:
    if tree.classify(tweet) == 'm':
        score += 1
    total+=1

print ('m score: ' + str(score/total))
