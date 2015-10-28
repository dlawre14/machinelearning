#Program for computing clustering on the language trigrams

import sys
import os
import itertools

def readInTrigrams(filename):
    '''
    Reads a language trigram file and returns a dictionary of trigram:count
    '''

    tricounts = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.split()
            tricounts[line[1]] = int(line[0])

    return tricounts

def distLang(l1, l2):
    '''
    l1, l2 are dictionaries of words and trigrams
    '''
    dist = 0
    keys = set()

    for key in l1:
        keys.add(key)
    for key in l2:
        keys.add(key)

    for key in keys:
        dist += abs(l1.get(key,0) - l2.get(key,0))

    return dist

def mergeFiles(f1name, f2name):
    f1tri = readInTrigrams('trigrams/'+f1name)
    f2tri = readInTrigrams('trigrams/'+f2name)

    keys = set()

    for key in f1tri:
        keys.add(key)
    for key in f2tri:
        keys.add(key)

    mergetri = {}

    for key in keys:
        mergetri[key] = f1tri.get(key,0) + f2tri.get(key,0)

    with open('trigrams/'+f1name.rstrip('.txt')+'_'+f2name.rstrip('.txt')+'.txt', 'w') as f:
        for key in mergetri:
            f.write(str(mergetri[key]) + ' ' + key + '\n')

    return


if __name__ == '__main__':
    #TODO: Write
