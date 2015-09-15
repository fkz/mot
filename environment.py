#!/usr/bin/env python

import random
import pygame
import sys

from motte import Motte
from motte import Allel
from motte import newChild
from settings import minMatingAge

from colorutils import colorDistance

backgroundColor = (255, 255, 255)
maxAge = 100
enemyVision = 0.25

class Cell:
  def __init__(self, neighborIndices):
    self.mot = None
    self.color = backgroundColor
    self.neighborIndices = neighborIndices
  
  def setMot(self, mot):
    self.mot = mot

def randomRGB():
  return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Environment:
  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.cells = {}
    self.numMots = 0
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
    assert(self.cells[mot.x,mot.y].mot == None)
    self.cells[mot.x, mot.y].setMot(mot)
    self.computeNeighbors(mot)
    for tom in mot.neighbors:
      self.computeNeighbors(tom)
    self.numMots += 1
    
  def removeMot(self, mot):
     assert(self.cells[mot.x, mot.y].mot != None)
     self.cells[mot.x, mot.y].mot = None
     for tom in mot.neighbors:
       self.computeNeighbors(tom)
     self.numMots -= 1
     assert(self.numMots >= 0)
     del(mot)
  
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

  def makeStripeColors(self):
    col1 = (255,255,0)
    col2 = (255,0,255)
    for x in range(0, self.width):
      for y in range(0, self.height):
        if (y >= self.height/2):
          self.cells[x,y].color = col1
        else:
          self.cells[x,y].color = col2

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
        pygame.draw.rect(screen, self.cells[x,y].color, (x * length, y * length,length,length), 0)
        if self.cells[x,y].mot != None:
          color = self.cells[x,y].mot.color
          ripeness = min(float(self.cells[x,y].mot.age) / float(minMatingAge), 1.0)
          adultRadius = length/2
          myRadius = max(int(ripeness * adultRadius), 4)
          pygame.draw.circle(screen, (0,0,0), (x * length + length/2, y*length + length/2), myRadius, 0)
          pygame.draw.circle(screen, color, (x * length + length/2, y*length + length/2), myRadius -1, 0)

          allelRadius = max(int(myRadius / 2) - 1, 1)
          color1 = self.cells[x,y].mot.allel1.rgb
          color2 = self.cells[x,y].mot.allel2.rgb
          pygame.draw.circle(screen, color1, (x * length + length/2 - allelRadius, y*length + length/2), allelRadius, 0)
          pygame.draw.circle(screen, color2, (x * length + length/2 + allelRadius, y*length + length/2), allelRadius, 0)

    pygame.display.update()

  def move(self, mot, dx, dy):
    newX = mot.x + dx; newY = mot.y + dy;
    if (newX >= 0 and newX < self.width and newY >= 0 and newY < self.height):
      if (self.cells[newX,newY].mot == None):
        self.cells[mot.x, mot.y].mot = None
        mot.x = newX; mot.y = newY;
        self.cells[mot.x, mot.y].setMot(mot)
        for tom in mot.neighbors:
          self.computeNeighbors(tom)
        self.computeNeighbors(mot)

  def mate(self, mot):
    potentialMates = []
    freePositions = []
    for (actX, actY) in self.cells[mot.x, mot.y].neighborIndices:
      if self.cells[actX, actY].mot != None:
        if self.cells[actX, actY].mot.doYouWantToMate():
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
       
        #someoneDies = random.randint(0,2)
        #if someoneDies > 0: # chance of 2/3 that someone dies during sex
        #  #randomly kill one of the partners
        #  poison = random.randint(0,1)
        #  #print "A mot died during sex." + " Now we have " + str(self.numMots-1) + " mots."
        #  if poison == 0:
        #    self.removeMot(mot)
        #  else:
        #    self.removeMot(partner)

        self.addMot(newMot)
        #print "A new mot was born on field (" + str(newMot.x) + ", " + str(newMot.y) + ")." + " Now we have " + str(self.numMots) + " mots."

  def step(self):
    #print "number of active mots: " + str(len(self.activeMots))
    #print "doing step with " + str(self.numMots) + " mots:"
    # initialize mating

    # move and age the mots
    for x in range(0, self.width):
      for y in range(0, self.height):
        if self.cells[x,y].mot != None:
          mot = self.cells[x,y].mot
          mot.hasMated = False
          for action in mot.step():
            action.executeAction(mot, self) 
          mot.age += 1
          if mot.age > maxAge:
            #print "A mot died of old age." + " Now we have " + str(self.numMots-1) + " mots."
            self.removeMot(mot)
          else:
            fitness = (colorDistance(self.cells[x,y].color, mot.color))
            isDying = random.randint(0,100)
            if isDying < int(fitness * enemyVision):
              #print "A mot was eaten by a grue. Mjammjam." + " Now we have " + str(self.numMots-1) + " mots."
              self.removeMot(mot)

    # check for mates
    for x in range(0, self.width):
      for y in range(0, self.height):
        if self.cells[x,y].mot != None:
          mot = self.cells[x,y].mot
          if mot.hasMated == False:
            self.mate(mot)

