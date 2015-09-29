#the naive bayes classifier

#how it works:
#we are looking for P(dialect|user) i.e. for a user, chance of dialect
#we use bayes law to say we can find P(user|dialect) * P(dialect) / P(user)
#we can throw out the denominator since it normalizes
#P(dialect) is simple, just take number of tweets to find
#so, now we just need P(user|dialect) this is P(w1|dialect) + P(w2|dialect) + ...
#wN is a word, so we find the probability of each word in the dialect, sum them
#then set this equal to P(user|dialect) fromt here we can solve for P(dialect|user)
#then just select maximum dialect

from math import log

class nbayes:

    def __init__(self):
        pass

    def classify(self, tweets, cwordprob, uwordprob, mwordprob, tokenize):
        cprob = 0
        uprob = 0
        mprob = 0
        #print ('<---------->')
        for tweet in tweets:
            for word in tokenize(tweet):
                #print ('curr c prob ' + str(cprob))
                cprob += log(cwordprob(word))
                uprob += log(uwordprob(word))
                mprob += log(mwordprob(word))
        return (cprob, uprob, mprob)
