#!/usr/bin/env python

import random
import pygame
import sys
import itertools

from motte import Motte
from motte import Allel
from motte import newChild
from settings import minMatingAge

from colorutils import colorDistance

backgroundColor = (255, 255, 255)

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

  def matesInView(self, mot):
    for (actX, actY) in self.cells[mot.x, mot.y].neighborIndices:
      if self.cells[actX, actY].mot != None:
        yield self.cells[actX, actY].mot
  
  def potentialMates(self, mot):
    return itertools.ifilter(doYouWantToMate, self.matesInView(mot))
  
  def freePositionsInView(self, mot):
    return itertools.ifilter(lambda ind: self.cells[ind].mot == None, self.cells[mot.x, mot.y].neighborIndices)

  def step(self):
    #print "number of active mots: " + str(len(self.activeMots))
    #print "doing step with " + str(self.numMots) + " mots:"
    # initialize mating

    # move and age the mots
    for x in range(0, self.width):
      for y in range(0, self.height):
        if self.cells[x,y].mot != None:
          mot = self.cells[x,y].mot
          for action in mot.step():
            action.executeAction(mot, self)
            
