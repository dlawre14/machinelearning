#the entry point for running decision tree code

import pickle
import operator
import random

from utility.entropy import entropy
from decisiontree.decisiontree import DecisionTree

import sys
import os

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

for key in utweets:
    trainingu.append(key)
for key in ctweets:
    trainingc.append(key)
for key in mtweets:
    trainingm.append(key)

words = set()
for key in trainingu:
  tweets = tree.tokenizetweets(utweets[key])
  tweets = [x for x in tweets]
  for tweet in tweets:
    if len(tweet) > 2 and len(tweet) < 8 and 'http' not in tweet and '#' not in tweet: words.add(tweet)
for key in trainingc:
  tweets = tree.tokenizetweets(ctweets[key])
  tweets = [x for x in tweets]
  for tweet in tweets:
    if len(tweet) > 2 and len(tweet) < 8 and 'http' not in tweet and '#' not in tweet: words.add(tweet)
for key in trainingm:
  tweets = tree.tokenizetweets(mtweets[key])
  tweets = [x for x in tweets]
  for tweet in tweets:
    if len(tweet) > 2 and len(tweet) < 8 and 'http' not in tweet and '#' not in tweet: words.add(tweet)

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

for user in os.listdir('decisiontree/dialects/test'):
  print (user)
  with open('decisiontree/dialects/test/' + user, 'r') as f:
    c = 0
    u = 0
    m = 0
    for line in f:
      classify = tree.classify(line)
      if classify == 'c':
        c+=1
      elif classify == 'u':
        u+=1
      else:
        m+=1
    print (user + ' -- ' + 'c: ' + str(c) + ' u: ' + str(u) + ' m: ' + str(m))
