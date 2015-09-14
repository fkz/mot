#!/usr/bin/env python

import random
import matplotlib.pylab as plt

mutationProbability = 0.10

class Allel:
  def __init__(self):
    self.rgb = (0, 0, 0)
    pass
  def random(self):
    self.rgb = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
  def mutate(self):
    pass
  def color(self):
    return self.rgb

class Motte:
  """
  A representation of a motte
  """
  def __init__(self, allel1, allel2):
    self.allel1 = allel1
    self.allel2 = allel2
    #self.color = (map allel1.rgb + allel2.rgb) / 2
  
  def randomAllel(self):
    if random.randint(0, 1) == 0:
      return self.allel1
    else:
      return self.allel2
  
def mutate(allel):
  a = random.uniform(0.0, 1.0)
  if (a < mutationProbability):
    allel.rgb = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

def newChild(motte1, motte2):
  assert(isInstance(motte1, Motte))
  return Motte(mutate(motte1.randomAllel()), mutate(motte2.randomAllel()))


class Environment:
  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.cells = {}
    for y in range(height):
      for x in range(width):
        self.cells[x,y] = None
  
  def generateRandom(self, count):
    realcount = 0
    for i in range(count):
      x = random.randint(0, self.width)
      y = random.randint(0, self.height)
      allel = Allel()
      allel.random()
      if self.cells[x,y] == None:
        realcount += 1
      self.cells[x,y] = allel

  def step(self):
    pass

if __name__ == "__main__":
  env = Environment(100,100)
      
