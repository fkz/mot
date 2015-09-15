#!/usr/bin/env python

import random
import pygame
import sys
from settings import mutationProbability, minMatingAge, maxAge, enemyVision
from colorutils import colorDistance
from creature import Creature, Action

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

class Motte(Creature):
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
    self.age += 1
    if self.age > maxAge:
      return [MotDies()]
    else:
       return [self.doMove(), PairWith()]

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
  def executeAction(self, mot, environment):
    matesInView = list(environment.matesInView(mot))
    freePositionsInView = list(environment.freePositionsInView(mot))
    try:
      partner = random.choice(matesInView)
      childPosition = random.choice(freePositionsInView)
      mating = random.randint(0,1)
      if mating == 1:
        newMot = newChild(mot, partner, childPosition[0], childPosition[1])
        environment.addMot(newMot)
    except IndexError:
      # there are no partners/no free positions
      pass

def newChild(motte1, motte2, x, y):
  return Motte(motte1.randomAllel().mutate(), motte2.randomAllel().mutate(), x, y, 0)
