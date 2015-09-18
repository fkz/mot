from statistics import Statistics
from livemotmonitor import MotsAlive
from colorutils import colorDistance
from motte import Motte

class Difference(MotsAlive):
  """
  the difference of colors to normal value
  """
  completeStatistics = 0
  count = 0
  
  def addMot(self, mot, env):
    #print "+1"
    #self.completeStatistics += self.difference(mot, env)
    self.count += 1

  def removeMot(self, mot, env):
    #print "-1"
    #self.completeStatistics -= self.difference(mot, env)
    self.count -= 1
  
  def step(self, env):
    self.completeStatistics = 0
    for pos in env.allCellPositions():
      mot = env.cells[pos][Motte]
      if mot != None:
        self.completeStatistics += self.difference(env.cells[pos][Motte], env)
    pass
    
  def info(self):
    count = self.count
    if count == 0:
      count = -1
    return "mots: {0}, diff: {1}".format(self.count, self.completeStatistics / count)

  def testValidity(self, env):
    count = 0
    stat = 0
    for pos in env.allCellPositions():
      mot = env.cells[pos][Motte]
      if mot != None:
        count += 1
#        stat += env.

  
  """
  the difference of the mot and 'the background'
  """
  def difference(self, mot, env):
    return colorDistance(mot.color, env.cells[mot.x,mot.y].color)
  
  def __enter__(self):
    return self
  
  def __exit__(self):
    pass

class DifferenceGraph(Difference):
  def __init__(self, env, filepath):
    super.__init__(env)
    self.outputfile = open(filepath, 'w')
  
  def step(self, env):
    super.step(env)
    self.completeStatistics = 0
    for pos in env.allCellPositions():
      self.completeStatistics += self.difference(env.cells[pos][Motte], env)
    self.outputfile.write("{0}, {1}".format(self.count, self.completeStatistics))
