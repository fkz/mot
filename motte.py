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
    self.count = 0

  def randomAllel(self):
    if random.randint(0, 1) == 0:
      return Allel(self.allel1.rgb)
    else:
      return Allel(self.allel2.rgb)
    
  def doYouWantToMate(self):
    return self.age >= minMatingAge
  
  def pair(self, environment):
    matesInView = list(environment.matesInView(self))
    freePositionsInView = list(environment.freePositionsInView(self))
    try:
      partner = random.choice(matesInView)
      childPosition = random.choice(freePositionsInView)
      mating = random.randint(0,1)
      if mating == 1:
        return PairWith(partner, childPosition)
      else:
        return None
    except IndexError:
      # there are no partners/no free positions
      return None

  
  def step(self, env):
    self.count += 1
    if self.count >= 4:
      self.count = 0
      if self.age > maxAge:
        yield MotDies()
      else:
        yield self.doMove()
        pairWith = self.pair(env)
        if pairWith != None:
          yield pairWith
        yield AddAge()

class MotDies(Action):
  def executeAction(self, mot, environment):
    environment.removeMot(mot)
  
class PairWith(Action):
  def __init__(self, partner, childPosition):
    self.partner = partner
    self.childPosition = childPosition
  """
  pair with an other mot
  """
  def executeAction(self, mot, environment):
    newMot = newChild(mot, self.partner, self.childPosition[0], self.childPosition[1])
    environment.addCreature(newMot)
    self.child = newMot
    
class AddAge(Action):
  def executeAction(self, mot, environment):
    mot.age += 1
    if mot.age <= minMatingAge:
      environment.cells[mot.x,mot.y].updated = True

def newChild(motte1, motte2, x, y):
  return Motte(motte1.randomAllel().mutate(), motte2.randomAllel().mutate(), x, y, 0)
