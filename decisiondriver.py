#the entry point for running decision tree code

import pickle
import operator
import random

from utility.entropy import entropy
from decisiontree.decisiontree import DecisionTree

import sys

#sys.setrecursionlimit(3500) #might be dangerous

tree = DecisionTree()

ctweets = None
utweets = None
mtweets = None

with open('ctweets', 'rb') as c, open('utweets', 'rb') as u, open('mtweets', 'rb') as m:
    ctweets = pickle.load(c)
    utweets = pickle.load(u)
    mtweets = pickle.load(m)

#Stripe tweets for testing
trainingu = [] #keys for training
trainingc = []
trainingm = []

testu = ['xx00','xx01']
testc = ['xx00','xx01']
testm = ['xx00','xx01']

for key in utweets:
  if key != 'xx00' and key != 'xx01':
    trainingu.append(key)
for key in ctweets:
  if key != 'xx00' and key != 'xx01':
    trainingc.append(key)
for key in mtweets:
  if key != 'xx00' and key != 'xx01':
    trainingm.append(key)

words = set()
for key in trainingu:
  tweets = tree.tokenizetweets(utweets[key])
  tweets = [x for x in tweets]
  for tweet in tweets:
    words.add(tweet)
for key in trainingc:
  tweets = tree.tokenizetweets(ctweets[key])
  tweets = [x for x in tweets]
  for tweet in tweets:
    words.add(tweet)
for key in trainingm:
  tweets = tree.tokenizetweets(mtweets[key])
  tweets = [x for x in tweets]
  for tweet in tweets:
    words.add(tweet)

print (len(words))

entkeyvals = []
for word in words:
  ccount = 0
  for key in trainingc:
    for tweet in ctweets[key]:
        if word in tweet.lower():
          ccount +=1
  ucount = 0
  for key in trainingu:
    for tweet in utweets[key]:
        if word in tweet.lower():
          ucount +=1
  mcount = 0
  for key in trainingm:
    for tweet in mtweets[key]:
        if word in tweet.lower():
          mcount +=1
  total = ccount + ucount + mcount
  if total > 0:
    ccount = ccount/total
    ucount = ucount/total
    mcount = mcount/total

    #print ('Calculating entropy for word: ' + word)

    ent = entropy([ccount,ucount,mcount])

    if ccount >= ucount and ccount >= mcount:
      entkeyvals.append((word,'c',ent))
    elif ucount >= ccount and ucount >= mcount:
      entkeyvals.append((word,'u',ent))
    else:
      entkeyvals.append((word,'m',ent))

entkeyvals = sorted(entkeyvals, key=operator.itemgetter(2))
entkeyvals.reverse()

tree.buildTree(tree.root, entkeyvals)

ccount = 0
uccount = 0
mcount = 0
for tweet in ctweets['xx00']:
  classify = tree.classify(tweet)
  if classify == 'c':
    ccount += 1
  elif classify == 'u':
    ucount += 1
  else:
    mcount += 1
print ('Classified ctweets')
print ('u: ' + str(ucount) + ' c: ' + str(ccount) + ' m: ' + str(mcount))

ccount = 0
uccount = 0
mcount = 0
for tweet in utweets['xx00']:
  classify = tree.classify(tweet)
  if classify == 'c':
    ccount += 1
  elif classify == 'u':
    ucount += 1
  else:
    mcount += 1
print ('Classified utweets')
print ('u: ' + str(ucount) + ' c: ' + str(ccount) + ' m: ' + str(mcount))

ccount = 0
uccount = 0
mcount = 0
for tweet in mtweets['xx00']:
  classify = tree.classify(tweet)
  if classify == 'c':
    ccount += 1
  elif classify == 'u':
    ucount += 1
  else:
    mcount += 1
print ('Classified mtweets')
print ('u: ' + str(ucount) + ' c: ' + str(ccount) + ' m: ' + str(mcount))
