#A class that allows easy definition of probabilities

class probability:

  def __init__(self):
    self._vals = {}

  def __call__(self, key):
    return self._vals[key]

  def addProb(self,key, prob):
    self._vals[key] = prob
