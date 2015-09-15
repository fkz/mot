#!/usr/bin/env python

import random
import pygame
import sys
from settings import mutationProbability, minMatingAge

class Allel:
  def __init__(self, rgb):
    self.rgb = rgb
  def mutate(self):
    a = random.uniform(0.0, 1.0)
    if (a < mutationProbability):
      rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
      return Allel(rgb)
    else:
      return Allel(self.rgb)

def mergeColor(rgb1, rgb2):
  return ((rgb1[0] + rgb2[0]) / 2, (rgb1[1] + rgb2[1]) / 2, (rgb1[2] + rgb2[2]) / 2)

class Motte:
  """
  A representation of a motte
  """
  def __init__(self, allel1, allel2, x, y, age):
    self.allel1 = allel1
    self.allel2 = allel2
    self.color = mergeColor(allel1.rgb, allel2.rgb)
    self.hasMated = False
    self.x = x
    self.y = y
    self.age = age
    self.neighbors = []

  def randomAllel(self):
    if random.randint(0, 1) == 0:
      return Allel(self.allel1.rgb)
    else:
      return Allel(self.allel2.rgb)
    
  def doYouWantToMate(self):
    return self.age >= minMatingAge
  
  def doMove(self):
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
    return MoveMot(dx, dy)

  
  def step(self):
    return [self.doMove()]

class Action:
  """
  an action is an interaction of a mot with the environment
  """
  def executeAction(self, mot, environment):
    assert True, "This is an abstract action"

class MotDies(Action):
  def executeAction(self, mot, environment):
    environment.removeMot(mot)
  
class MoveMot(Action):
  """
  move in some direction if possible
  """
  def __init__(self, dx, dy):
    self.dx = dx
    self.dy = dy
  def executeAction(self, mot, environment):
    environment.move(mot, self.dx, self.dy)

class PairWith(Action):
  """
  pair with an other mot
  """
  def __init__(self, otherMot, positionOfNewChild):
    self.otherMot = otherMot
    self.positionOfNewChild = positionOfNewChild

def newChild(motte1, motte2, x, y):
  return Motte(motte1.randomAllel().mutate(), motte2.randomAllel().mutate(), x, y, 0)
