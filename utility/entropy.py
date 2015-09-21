#Utility for calculating the shannon entropy value
from math import log

def entropy(args):
    value = 0
    for x in args:
      if x > 0:
        value += -(x * log(x, 2))
    return value

def gain(ents, weights):
    #a list of entropies and a list of weights
    output = 0
    for x,y in zip(ents,weights):
        output += (x*y)
    return output

def calcprob(counts):
    #a list of counts
    s = sum(counts)
    for i in range(len(counts)):
        counts[i] /= s

    return counts

if __name__ == '__main__':
    pass
