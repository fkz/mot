#!/usr/bin/env python

import random
import pygame
import sys

from motte import Motte
from motte import Allel

backgroundColor = (37, 172, 118)

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

  def move(self, mot, x, y):
    mot.hasMoved = True
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
    newX = x + dx; newY = y + dy;
    if (newX >= 0 and newX < self.width and newY >= 0 and newY < self.height):
      if (self.cells[newX,newY].mot == None):
        self.cells[x,y].mot = None
        self.cells[newX, newY].mot = mot

  def step(self):
    for x in range(0, self.width):
      for y in range(0, self.height):
        if self.cells[x,y].mot != None:
          self.cells[x,y].mot.hasMoved = False

    for x in range(0, self.width):
      for y in range(0, self.height):
        if self.cells[x,y].mot != None and self.cells[x,y].mot.hasMoved == False:
          self.move(self.cells[x,y].mot, x, y)
