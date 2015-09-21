#code for making and training a decision tree and querying for classification
import os
import pickle

class Node:

  def __init__(self, parent = None):
    self.parent = parent
    self.word = None
    self.yes = None #could be a node or an outcome
    self.no = None

class DecisionTree:

    def __init__(self):
        self.root = Node()

    #Note: only needs to be done once
    def read_data(self, udir, mdir, cdir, **kwargs):
        shouldpickle = kwargs.get('pickle', False)

        ulist = os.listdir(udir)
        mlist = os.listdir(mdir)
        clist = os.listdir(cdir)

        usertweetsu = {}
        usertweetsm = {}
        usertweetsc = {}

        for user in ulist:
            usertweetsu[user] = []
            with open(udir + user, 'r') as f:
                for line in f:
                    usertweetsu[user].append(line.rstrip('\n'))
        for user in clist:
            usertweetsc[user] = []
            with open(cdir + user, 'r') as f:
                for line in f:
                    usertweetsc[user].append(line.rstrip('\n'))
        for user in mlist:
            usertweetsm[user] = []
            with open(mdir + user, 'r') as f:
                for line in f:
                    usertweetsm[user].append(line.rstrip('\n'))

        with open('utweets', 'wb') as u, open('ctweets', 'wb') as c, open('mtweets', 'wb') as m:
            pickle.dump(usertweetsu, u)
            pickle.dump(usertweetsc, c)
            pickle.dump(usertweetsm, m)

    #Takes a list of all tweets by a user and tokenizes them
    #modes: whitespace, nort, noat, nortnoat
    def tokenizetweets(self, tweets, mode='whitespace'):
        tokens = {}
        for entry in tweets:
            entry = entry.lower()
            if mode == 'nort' or mode == 'nortnoat': #remove retweets
                entry = entry.lstrip('RT ')

            tok = entry.split()
            for t in tok:
                if mode == 'noat' or mode == 'nortnoat':
                    if '@' in t:
                        pass
                    else:
                        tokens[t] = tokens.get(t, 0) + 1
                else:
                    tokens[t] = tokens.get(t, 0) + 1

        return tokens

    #takes a list of tokens and frequenices (in list(tuple)) and throws away
    #selected tuples the user doesn't want
    def tokencleaner(self, tokens, **kwargs):
        for i in range(len(tokens)):
            if kwargs.get('nourl', False):
                if ('http://' in tokens[i][0]):
                    tokens[i] = '@@@@@@@@@@@@@@@@'

    def buildTree(self, currNode, tokens):
      #TODO: build tree list is in the form [(word, class, entropy)]
      #should be sorted

      #doing this with a loop to fix recursion problem

      for tup in tokens:
        if tokens.index(tup) == len(tokens) - 1:
          currNode.parent.no = tup[1]
          print ('We are out of words')
          return

        currNode.yes = tup[1]
        currNode.no = Node(currNode)
        currNode.word = tup[0]

        currNode = currNode.no

    def printtree(self, currNode=None):
        while type(currNode) != str:
          print (currNode.word + ' yes -> ' + currNode.yes)
          currNode = currNode.no

    def classify(self, tweet):
        tweet = tweet.lower().split()
        currNode = self.root
        while type(currNode) is Node:
            #print ('Checking if ' + currNode.word + ' is in tweet...')
            if currNode.word in tweet:
                #print ('Word found, returning classification...')
                #print ('Found word ' + currNode.word + ' in tweet classifying as: ' + currNode.yes)
                return currNode.yes
            else:
                #print ('Word not found, recursing...')
                currNode = currNode.no
        #at end
        #print ('Found no word match, classifying as: m')
        return currNode
