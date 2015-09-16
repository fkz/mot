#!/usr/bin/env python

import random
import pygame
import sys
import itertools

from motte import Motte
from motte import Allel
from motte import newChild
from settings import minMatingAge, probabilityEagle
from eagle import Eagle

from colorutils import colorDistance, randomRGB

backgroundColor = (255, 255, 255)

VALID_TYPES = [Motte, Eagle]

class Cell:
  def __init__(self, x, y, neighborIndices):
    self.x = x
    self.y = y
    self.creatures = [None] * len(VALID_TYPES)
    self.updated = True
    self.updatedEagle = False
    if random.randrange(100) < probabilityEagle:
      self[Eagle] = Eagle(x, y)
    self.color = backgroundColor
    self.neighborIndices = neighborIndices
  def __getitem__(self, t):
    for idx, val in enumerate(VALID_TYPES):
      if val == t:
        return self.creatures[idx]
  def __setitem__(self, t, value):
    for idx, val in enumerate(VALID_TYPES):
      if val == t:
        self.creatures[idx] = value
    if (t == Eagle) and self.updated == False:
      self.updatedEagle = True
    else:
      self.updated = True
  def setCreature(self, creature):
    self[type(creature)] = creature
  def allCreatures(self):
    for creature in self.creatures:
      if creature != None:
        yield creature

class Environment:
  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.cells = {}
    self.numMots = 0
    for y in range(height):
      for x in range(width):
        self.cells[x,y] = Cell(x, y, self.neighborIndices(x,y))

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
      if self.cells[x,y][Motte] != None:
        mot.neighbors.append(self.cells[x,y][Motte])

  def addCreature(self, creature):
    assert(self.cells[creature.x,creature.y][type(creature)] == None)
    self.cells[creature.x, creature.y].setCreature(creature)
    self.numMots += 1

  def removeMot(self, mot):
     assert(self.cells[mot.x, mot.y][Motte] != None)
     self.cells[mot.x, mot.y][Motte] = None
     self.numMots -= 1
     assert(self.numMots >= 0)
     del(mot)
  
  def generateRandom(self, count):
    realcount = 0
    for i in range(count):
      x = random.randint(0, self.width - 1)
      y = random.randint(0, self.height - 1)
      if self.cells[x,y][Motte] == None:
        realcount += 1
        allel1 = Allel(randomRGB())
        allel2 = Allel(randomRGB())
        mot = Motte(allel1, allel2, x, y, 0)
        self.addCreature(mot)

  def makeStripeColors(self, col1, col2):
    for x in range(0, self.width):
      for y in range(0, self.height):
        if (y >= self.height/2):
          self.cells[x,y].color = col1
        else:
          self.cells[x,y].color = col2
        self.cells[x,y].updated = True

  def move(self, creature, dx, dy):
    newX = creature.x + dx; newY = creature.y + dy;
    typeOfCreature = type(creature)
    if (newX >= 0 and newX < self.width and newY >= 0 and newY < self.height):
      if (self.cells[newX,newY][typeOfCreature] == None):
        self.cells[creature.x, creature.y][typeOfCreature] = None
        creature.x = newX; creature.y = newY;
        self.cells[creature.x, creature.y].setCreature(creature)

  def matesInView(self, mot):
    for (actX, actY) in self.cells[mot.x, mot.y].neighborIndices:
      if self.cells[actX, actY][Motte] != None:
        yield self.cells[actX, actY][Motte]
  
  def potentialMates(self, mot):
    return itertools.ifilter(doYouWantToMate, self.matesInView(mot))
  
  def freePositionsInView(self, mot):
    return itertools.ifilter(lambda ind: self.cells[ind][Motte] == None, self.cells[mot.x, mot.y].neighborIndices)

  def stepWithAge(self):
    for x in range(0, self.width):
      for y in range(0, self.height):
        for creature in self.cells[x,y].allCreatures():
          for action in creature.step(self):
            action.executeAction(creature, self)
            yield creature, action

  def step(self):
    list(self.stepWithAge())