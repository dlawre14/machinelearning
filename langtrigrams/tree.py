import pickle

from graphviz import Digraph

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
    for n in nodes:
      if n.parent and n.parent.val == curr.val:
        curr.addchild(treenode(n.val, curr))
        jobs.append(curr.getchildren()[len(curr.getchildren())-1])

  #do full trace

  graphlist = {}
  nodeid = {}

  locals = [root]
  i = 0
  while len(locals) != 0:
    curr = locals.pop()
    #print ('curr: ' + str(curr) + ' parent: ' + str(curr.parent))
    locals += list(curr.getchildren())

    graphlist[i] = curr
    nodeid[curr] = i
    i+=1

  dot = Digraph(comment='lang phylo tree')

  #Note: tree contains 199 nodes
  i -= 1
  for j in range(i):
    print (graphlist[j].val)
    dot.node(str(j), graphlist[j].val)

  for nd in nodeid:
    children = nd.getchildren()
    if len(children) == 2:
      dot.edge(str(nodeid[nd]), str(nodeid[children[0]]))
      dot.edge(str(nodeid[nd]), str(nodeid[children[1]]))

  dot.render('tree.gv', view=True)
