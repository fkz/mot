#!/usr/bin/env python

import random

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
    self.color = (map (lambda x, y: (x + y) / 2), allel1.color(), allel2.color())

  def randomAllel(self):
    if random.randint(0, 1) == 0:
      return self.allel1
    else:
      return self.allel2

def newChild(motte1, motte2):
  assert(isInstance(motte1, Motte))
  return Motte(motte1.randomAllel(), motte2.randomAllel)

class Environment:
  def __init__(self, height, width):
    self.height = height
    self.width = width
    for y in range(height):
      for x in range(width):
        self.cells[y][x] = None

  def generateRandom(self, count):
    realcount = 0
    for i in range(count):
      x = random.randint(0, self.width)
      y = random.randint(0, self.height)
      allel = Allel()
      allel.random()
      if self.cells[x][y] == None:
        realcount += 1
      self.cells[x][y] = allel

