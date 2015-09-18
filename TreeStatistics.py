
from statistics import Statistics
from motte  import PairWith, Motte

class TreeStatistics(Statistics):
  def __init__(self, env, filepath):
    self.filepath = filepath
    # initialize first mots
    self.outputFile = open(self.filepath, 'w')
    self.outputFile.write("digraph HI {\n")
    for x in range(0, env.width):
      for y in range(0, env.height):
        mot = env.cells[x,y][Motte]
        if mot != None:
          self.motNames[mot] = self.index
          self.motsInCurrentGeneration.append("c{0}".format(self.index))
          self.index += 1
          self.addMod(mot)
    self.outputStr += "{{rank=same {0}}}".format(" ".join(self.motsInCurrentGeneration))
    self.motsInCurrentGeneration = []

  motNames = {}
  motsInCurrentGeneration = []
  outputStr = ""
  index = 0

  def addMod(self, mod):
    name = "c{0}".format(self.motNames[mod])
    self.outputFile.write("{}[fillcolor=\"#{:02X}{:02X}{:02X}\" style=filled]\n".format(name, mod.color[0], mod.color[1], mod.color[2]))

  def __enter__(self):
    return self
  
  def __exit__(self):
    self.outputFile.write(self.outputStr)
    self.outputFile.write("}\n")
    self.outputFile.close()
  
  def step(self, env):
    #self.outputStr += "->"
    self.outputStr += "{{rank=same {0}}}".format(" ".join(self.motsInCurrentGeneration))
    self.motsInCurrentGeneration = []
  
  def mergeAction(self, env, creature, action):
    if isinstance(action, PairWith):
      newIndex = self.index
      self.index += 1
      self.motNames[action.child] = newIndex
      self.addMod(action.child)
      color1 = "#{:02X}{:02X}{:02X}".format(action.child.allel1.rgb[0], action.child.allel1.rgb[1], action.child.allel1.rgb[2])
      color2 = "#{:02X}{:02X}{:02X}".format(action.child.allel2.rgb[0], action.child.allel2.rgb[1], action.child.allel2.rgb[2])
      self.outputFile.write("c{0} -> c{2}[color=\"{3}\"]\nc{1} -> c{2}[color=\"{4}\"]\n".format(self.motNames[creature], self.motNames[action.partner], newIndex, color1, color2))
      self.motsInCurrentGeneration.append("c{0}".format(newIndex))
  