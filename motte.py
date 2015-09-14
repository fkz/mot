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

class Cell:
  def __init__(self):
    self.mot = None
    self.color = backgroundColor
  
  def setMot(self, mot):
    self.mot = mot
    self.color = mot.color

class Environment:
  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.cells = {}
    for y in range(height):
      for x in range(width):
        self.cells[x,y] = Cell()
  
  def generateRandom(self, count):
    realcount = 0
    for i in range(count):
      x = random.randint(0, self.width - 1)
      y = random.randint(0, self.height - 1)
      allel1 = Allel()
      allel1.random()
      allel2 = Allel()
      allel2.random()
      mot = Motte(allel1, allel2)
      if self.cells[x,y].mot == None:
        realcount += 1
      self.cells[x,y].setMot(mot)

  def step(self):
    pass

def drawEnvironment(screen, env):
  screenWidth = screen.get_width()
  screenHeight = screen.get_height()
  envWidth = env.width
  envHeight = env.height
  cellDim = max(envWidth, envHeight)
  screenDim = min(screenWidth, screenHeight)
  length = screenDim / (cellDim)
  for x in range(0, envWidth):
    for y in range(0, envHeight):
      if env.cells[x,y] != None:
        color = env.cells[x,y].color
      else:
        color = backgroundColor
      pygame.draw.rect(screen, (0,0,0), (x * length-1, y * length-1,length+2,length+2), 0)
      pygame.draw.rect(screen, backgroundColor, (x * length, y * length,length,length), 0)
      pygame.draw.circle(screen, color, (x * length - length/2, y*length - length/2), length/2 -1, 0)
  pygame.display.update()

if __name__ == "__main__":
  pygame.init()
  env = Environment(10,10)
  env.generateRandom(20)
  screen = pygame.display.set_mode((1000,1000))
  env.draw(screen)
  pygame.display.update()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit(); sys.exit();
