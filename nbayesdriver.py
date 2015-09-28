#main entry for naive bayes of irish tweets
import os

from utility.prob import probability
from utility.tokenize import tokenize

utweets = {}
ctweets = {}
mtweets = {}

root = 'nbayes/dialects/'
for user in os.listdir(root+'u/'):
    with open(root+'u/'+user,'r') as f:
        tweets = []
        for line in f:
            tweets.append(line.rstrip('\n'))
        utweets[user] = tweets
for user in os.listdir(root+'c/'):
    with open(root+'c/'+user,'r') as f:
        tweets = []
        for line in f:
            tweets.append(line.rstrip('\n'))
        ctweets[user] = tweets
for user in os.listdir(root+'m/'):
    with open(root+'m/'+user,'r') as f:
        tweets = []
        for line in f:
            tweets.append(line.rstrip('\n'))
        mtweets[user] = tweets

#just count users
sumu = 0
sumc = 0
summ = 0

for key in utweets:
    sumu+=1
for key in ctweets:
    sumc+=1
for key in mtweets:
    summ+=1

total = sumu+sumc+summ

#proability a user is a dialect
probu = sumu/total
probc = sumc/total
probm = summ/total

dialectprob = probability()
dialectprob.addProb('u', probu)
dialectprob.addProb('c', probc)
dialectprob.addProb('m', probm)

for key in utweets:
    occur = {}
    for tweet in utweets[key]:
        tokens = tokenize(tweet)
        for token in tokens:
            occur[token] = occur.get(token, 0) + 1
    utweets[key] = occur
for key in ctweets:
    occur = {}
    for tweet in ctweets[key]:
        tokens = tokenize(tweet)
        for token in tokens:
            occur[token] = occur.get(token, 0) + 1
    ctweets[key] = occur
for key in mtweets:
    occur = {}
    for tweet in mtweets[key]:
        tokens = tokenize(tweet)
        for token in tokens:
            occur[token] = occur.get(token, 0) + 1
    mtweets[key] = occur

allwords = set()

for key in ctweets:
    for word in ctweets[key]:
        allwords.add(word)

print (allwords)
