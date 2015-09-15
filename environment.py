#!/usr/bin/env python

import random
import pygame
import sys

from motte import Motte
from motte import Allel
from motte import newChild

backgroundColor = (37, 172, 118)
maxAge = 10
minMatingAge = 6

class Cell:
  def __init__(self, neighborIndices):
    self.mot = None
    self.color = backgroundColor
    self.neighborIndices = neighborIndices
  
  def setMot(self, mot):
    self.mot = mot
    self.color = mot.color

def randomRGB():
  return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Environment:
  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.mots = []
    self.cells = {}
    for y in range(height):
      for x in range(width):
        self.cells[x,y] = Cell(self.neighborIndices(x,y))

  def neighborIndices(self, x,y):
    indices = []
    for dx in [-1,0,1]:
      for dy in [-1,0,1]:
        if dx == 0 and dy == 0:
          continue
        newX = x + dx; newY = y + dy;
        if newX >= 0 and newX < self.width and newY >= 0 and newY < self.height:
          indices.append((newX, newY))
    return indices

  def computeNeighbors(self, mot):
    mot.neighbors = []
    for (x,y) in self.cells[mot.x, mot.y].neighborIndices:
      if self.cells[x,y].mot != None:
        mot.neighbors.append(self.cells[x,y].mot)

  def addMot(self, mot):
    self.cells[mot.x, mot.y].setMot(mot)
    self.mots.append(mot)
    self.computeNeighbors(mot)
    for tom in mot.neighbors:
      self.computeNeighbors(tom)
    
  def removeMot(self, mot):
     self.cells[mot.x, mot.y].mot = None
     for tom in mot.neighbors:
       oldNum = len(tom.neighbors)
       self.computeNeighbors(tom)
     self.mots.remove(mot)
  
  def generateRandom(self, count):
    realcount = 0
    for i in range(count):
      x = random.randint(0, self.width - 1)
      y = random.randint(0, self.height - 1)
      if self.cells[x,y].mot == None:
        realcount += 1
        allel1 = Allel(randomRGB())
        allel2 = Allel(randomRGB())
        mot = Motte(allel1, allel2, x, y, 0)
        self.addMot(mot)

  def draw(self, screen):
    screenWidth = screen.get_width()
    screenHeight = screen.get_height()
    envWidth = self.width
    envHeight = self.height
    cellDim = max(envWidth, envHeight)
    screenDim = min(screenWidth, screenHeight)
    length = screenDim / (cellDim)
    for x in range(0, envWidth):
      for y in range(0, envHeight):
        pygame.draw.rect(screen, (0,0,0), (x * length-1, y * length-1,length+2,length+2), 0)
        pygame.draw.rect(screen, backgroundColor, (x * length, y * length,length,length), 0)
        if self.cells[x,y].mot != None:
          color = self.cells[x,y].mot.color
          pygame.draw.circle(screen, (0,0,0), (x * length + length/2, y*length + length/2), length/2, 0)
          pygame.draw.circle(screen, color, (x * length + length/2, y*length + length/2), length/2 -1, 0)
    pygame.display.update()

  def move(self, mot):
    dx = 0; dy = 0;
    direction = random.randint(0, 3)
    if direction == 0: # try up
      dy = -1
    elif direction == 1: # try down
      dy = 1
    elif direction == 2: # try left
      dx = -1
    else: # try right
      dx = +1
    newX = mot.x + dx; newY = mot.y + dy;
    if (newX >= 0 and newX < self.width and newY >= 0 and newY < self.height):
      if (self.cells[newX,newY].mot == None):
        self.removeMot(mot)
        mot.x = newX; mot.y = newY;
        self.addMot(mot)

  def mate(self, mot):
    potentialMates = []
    freePositions = []
    for (actX, actY) in self.cells[mot.x, mot.y].neighborIndices:
      if self.cells[actX, actY].mot != None:
        if self.cells[actX, actY].mot.age >= minMatingAge:
          potentialMates.append(self.cells[actX, actY].mot)
      else:
        freePositions.append((actX, actY))
    if len(potentialMates) > 0 and len(freePositions) > 0:
      partner = potentialMates[random.randint(0, len(potentialMates) - 1)]
      mating = random.randint(0,1)
      if mating == 1:
        if len(freePositions) > 1:
          newPos = freePositions[random.randint(0, len(freePositions) - 1)]
        else:
          newPos = freePositions[0]
        newMot = newChild(mot, partner, newPos[0], newPos[1])
        mot.hasMated = True; partner.hasMated = True;
        # randomly kill one of the partners
        poison = random.randint(0,1)
        if poison == 0:
          self.removeMot(mot)
        else:
          self.removeMot(partner)

        self.addMot(newMot)
        #print "A new mot was born on field (" + str(newMot.x) + ", " + str(newMot.y) + ")."

  def step(self):
    #print "number of active mots: " + str(len(self.activeMots))
    #print "doing step with " + str(len(self.mots)) + " mots:"
    # initialize mating
    for mot in self.mots:
      mot.hasMated = False
    # age the mots
    for mot in self.mots:
      mot.age += 1
      if (mot.age > maxAge):
        self.removeMot(mot)
        #print "A mot died of old age."
    # move the mots
    for mot in self.mots:
      self.move(mot)
    # check for mates
    for mot in self.mots:
      if mot.hasMated == False and mot.age >= minMatingAge:
        pass
        self.mate(mot)

