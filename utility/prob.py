#A class that allows easy definition of probabilities

class probability:

  def __init__(self):
    self._vals = {}

  def __call__(self, key):
    if key not in self._vals:
        return 0.0000001
    return self._vals[key]

  def addProb(self,key, prob):
    if prob == 0:
        self._vals[key] = 0.000001
    else:
        self._vals[key] = prob
