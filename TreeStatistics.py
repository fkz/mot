
from statistics import Statistics
from motte  import PairWith, Motte

class TreeStatistics(Statistics):
  def __init__(self, env, filepath):
    self.filepath = filepath
    # initialize first mots
    self.index = 0
   
        
  motNames = {}
  index = 0
  
  def __enter__(self):
    self.outputFile = open(self.filepath, 'w')
    self.outputFile.write("digraph HI {\n")
    for x in range(0, env.width):
      for y in range(0, env.height):
        mot = env.cells[x,y][Motte]
        if mot != None:
          self.motNames[mot] = self.index
          self.index += 1

    return self
  
  def __exit__(self):
    self.outputFile.write("}\n")
    self.outputFile.close()
  
  def step(self, env):
    pass
  
  def mergeAction(self, env, creature, action):
    if isinstance(action, PairWith):
      newIndex = self.index
      self.index += 1
      self.motNames[action.child] = newIndex
      self.outputFile.write("c{0} -> c{2}\nc{1} -> c{2}\n".format(self.motNames[creature], self.motNames[action.partner], newIndex))
  
  