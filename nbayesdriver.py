#main entry for naive bayes of irish tweets
import os
import re

from math import log

from utility.prob import probability
from utility.tokenize import tokenize

from nbayes.nbayes import nbayes

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
sumcwords = 0
sumuwords = 0
summwords = 0

for key in ctweets:
    for word in ctweets[key]:
        sumcwords += ctweets[key][word]
        allwords.add(word)
for key in utweets:
    for word in utweets[key]:
        sumuwords += utweets[key][word]
        allwords.add(word)
for key in mtweets:
    for word in mtweets[key]:
        summwords += mtweets[key][word]
        allwords.add(word)

#probability of a word given the dialect
wordprobc = probability()
wordprobu = probability()
wordprobm = probability()

for word in allwords:
    count = 0
    for user in ctweets:
        count += ctweets[user].get(word, 0)
    #print ('Count of ' + word + ' in c is ' + str(count))
    if count/sumcwords > 0.001:
        wordprobc.addProb(word, count/sumcwords)

    count = 0
    for user in utweets:
        count += utweets[user].get(word, 0)
    #print ('Count of ' + word + ' in u is ' + str(count))
    if count/sumuwords > 0.001:
        wordprobu.addProb(word, count/sumuwords)

    count = 0
    for user in mtweets:
        count += mtweets[user].get(word, 0)
    #print ('Count of ' + word + ' in m is ' + str(count))
    if count/summwords > 0.001:
        wordprobm.addProb(word, count/summwords)

nb = nbayes()
print ('\tc-dia\t\t\tu-dia\t\t\tm-dia')
for user in os.listdir('nbayes/dialects/test'):
    with open('nbayes/dialects/test/'+user, 'r') as f:
        lines = f.readlines()
        lines = [x.rstrip('\n') for x in lines]
        classtup = nb.classify(lines, wordprobc, wordprobu, wordprobm, tokenize)
        classtup = (classtup[0]+log(dialectprob('c')), classtup[1]+log(dialectprob('u')), classtup[2]+log(dialectprob('m')))
        classify = ''
        index =' max: ' + str(classtup.index(max(classtup)))
        index = re.sub('max: 0', 'class: c', index)
        index = re.sub('max: 1', 'class: u', index)
        index = re.sub('max: 2', 'class: m', index)
        print (user + str(classtup) + index)
