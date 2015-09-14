#!/usr/bin/env python

import random
import pygame
import sys

mutationProbability = 0.10
backgroundColor = (37, 172, 118)

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
    self.color = map (lambda x, y: (x + y) / 2, allel1.color(), allel2.color())

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
