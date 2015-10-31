import pickle

class node:

  def __init__(self, val):
    self.val = val
    self.parent = None

  def setparent(self, parent):
    #parent is a node
    self.parent = parent

  def getparent(self):
    return self.parent

  def __repr__(self):
    return '<'+self.val+'>'

class treenode:

  def __init__(self, val, parent):
    self.val = val
    self.parent = parent
    self.children = [] #trivially 2 but left/right is arbitrary

  def addchild(self, child):
    #child should be a node
    self.children.append(child)

  def getchild(self, child):
    return self.children[self.children.index(child)]

  def getchildren(self):
    return self.children

  def __repr__(self):
    return '<'+self.val+'>'

def findnode(nodes, target):
  #print ('finding target: ' + str(target))
  for i in range(len(nodes)):
    if nodes[i].val == target:
      return i

if __name__ == '__main__':
  data = pickle.load(open('tree.p', 'rb'))
  #split data

  nodes = []

  for key in data:
    nodes.append(node(key))

  nodes.append(node('98.txt')) #this is our root

  for n in nodes:
    if n.val == '98.txt':
      pass
    else:
      parent = data[n.val]
      ind = findnode(nodes, str(parent)+'.txt')
      n.setparent(nodes[ind])

  root = treenode('98.txt', None)

  for n in nodes:
    if n.parent and n.parent.val == '98.txt':
      root.addchild(treenode(n.val, root))

  jobs = list(root.getchildren())

  while len(jobs) != 0:
    curr = jobs.pop()
    print (curr)
    for n in nodes:
      if n.parent and n.parent.val == curr.val:
        curr.addchild(treenode(n.val, curr))
        jobs.append(curr.getchildren()[len(curr.getchildren())-1])

  #TODO: somehow visualize the tree
