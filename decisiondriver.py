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
usersc = []
for key in ctweets:
    usersc.append(key)

trainingc = usersc[0:17]
testc = usersc[17:19]

trainingc = [ctweets[x] for x in trainingc]
testc = [ctweets[x] for x in testc]

temp = []
for entry in trainingc:
    temp += entry
trainingc = list(temp)
temp = []
for entry in testc:
    temp += entry
testc = list(temp)
##
usersu = []
for key in utweets:
    usersu.append(key)

trainingu = usersu[0:21]
testu = usersu[21:24]

trainingu = [utweets[x] for x in trainingu]
testu = [utweets[x] for x in testu]

temp = []
for entry in trainingu:
    temp += entry
trainingu = list(temp)
temp = []
for entry in testu:
    temp += entry
testu = list(temp)
##
usersm = []
for key in mtweets:
    usersm.append(key)

trainingm = usersm[0:5]
testm = usersm[5:7]

trainingm = [mtweets[x] for x in trainingm]
testm = [mtweets[x] for x in testm]

temp = []
for entry in trainingm:
    temp += entry
trainingm = list(temp)
temp = []
for entry in testm:
    temp += entry
testm = list(temp)

#create dictionaries of tokens
utokens = tree.tokenizetweets(trainingu)
ctokens = tree.tokenizetweets(trainingc)
mtokens = tree.tokenizetweets(trainingm)

utokens = {x:y for x,y in utokens.items() if utokens[x] > 2}
ctokens = {x:y for x,y in ctokens.items() if ctokens[x] > 2}
mtokens = {x:y for x,y in mtokens.items() if mtokens[x] > 2}

allkeys = set()
for key in utokens:
  allkeys.add(key)
for key in ctokens:
  allkeys.add(key)
for key in mtokens:
  allkeys.add(key)

entkeyvals = []
#total = len(allkeys)
for key in allkeys:
  total = utokens.get(key,0) + ctokens.get(key,0) + mtokens.get(key,0)

  uprob = utokens.get(key,0)/total
  cprob = ctokens.get(key,0)/total
  mprob = mtokens.get(key,0)/total

  classify = 'u'
  if cprob >= uprob and cprob >= mprob:
    classify = 'c'
  elif uprob >= cprob and uprob >= mprob:
    classify = 'u'
  else:
    classify = 'm'

  ent = entropy([uprob,cprob,mprob])
  if len(key) > 1:
    entkeyvals.append((key, classify, ent))

entkeyvals = sorted(entkeyvals, key=operator.itemgetter(2))
entkeyvals.reverse()

tree.buildTree(tree.root, entkeyvals)

mcount = 0
ccount = 0
ucount = 0

for tweet in testm:
    out = tree.classify(tweet)
    if out == 'm':
        mcount+=1
    if out == 'c':
        ccount+=1
    if out == 'u':
        ucount+=1

print ('c classify: ' + str(ccount))
print ('u classify: ' + str(ucount))
print ('m classify: ' + str(mcount))
