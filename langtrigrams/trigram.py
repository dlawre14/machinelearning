#Program for computing clustering on the language trigrams

import sys
import os
import itertools

import time
import pickle

def readInTrigrams(filename, probconv=True):
    '''
    Reads a language trigram file and returns a dictionary of trigram:count
    '''

    tricounts = {}
    total = 0
    with open(filename, 'r') as f:
        for line in f:
            line = line.split()
            tricounts[line[1]] = int(line[0])
            total += int(line[0])

    if probconv:
        for key in tricounts:
            tricounts[key] = tricounts[key]/total

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

def mergeFiles(f1name, f2name, outname):
    f1tri = readInTrigrams('trigrams/'+f1name, False)
    f2tri = readInTrigrams('trigrams/'+f2name, False)

    keys = set()

    for key in f1tri:
        keys.add(key)
    for key in f2tri:
        keys.add(key)

    mergetri = {}

    for key in keys:
        mergetri[key] = f1tri.get(key,0) + f2tri.get(key,0)

    with open('trigrams/'+outname, 'w') as f:
        for key in mergetri:
            f.write(str(mergetri[key]) + ' ' + key + '\n')

    return


if __name__ == '__main__':
    #Generate root dist matrix
    start = time.time()
    langs = os.listdir('trigrams')

    parentalid = {}

    while len(langs) > 1:
        minpair = None
        mindist = 1000000000000000
        for pairs in itertools.combinations(langs, 2):
            l1 = readInTrigrams('trigrams/'+pairs[0])
            l2 = readInTrigrams('trigrams/'+pairs[1])
            dist = distLang(l1,l2)
            if dist < mindist:
                mindist = dist
                minpair = (pairs[0], pairs[1])

        print ('Pairing ' + str(minpair) + ' langs left ' + str(len(langs)-1))

        mergeFiles(minpair[0], minpair[1], str(100 - len(langs))+'.txt')

        with open('mergehist.txt', 'a') as f:
            f.write('Merge #' + str(len(langs) - 100) + ' ' + minpair[0] + ' ' + minpair[1] + '\n')
        with open('nameref.txt', 'a') as f:
            f.write('Pairing ' + str(minpair) + ' --> ' + str(100 - len(langs))+'.txt\n')

        parentalid[minpair[0]] = 100 - len(langs)
        parentalid[minpair[1]] = 100 - len(langs)

        langs.append(str(100 - len(langs))+'.txt')
        langs.remove(minpair[0])
        langs.remove(minpair[1])

    pickle.dump(parentalid, open('tree.p', 'wb'))
