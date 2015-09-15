#!/usr/bin/env python

import random
import pygame
import sys
from settings import mutationProbability

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

class Action:
  """
  an action is an interaction of a mot with the environment
  """

class MotDies(Action):
  
class MoveMot(Action):
  """
  move in some direction if possible
  """
  def __init__(self, dx, dy):
    self.dx = dx
    self.dy = dy

class PairWith(Action):
  """
  pair with an other mot
  """
  def __init__(self, otherMot, positionOfNewChild):
    self.otherMot = otherMot
    self.positionOfNewChild = positionOfNewChild

def newChild(motte1, motte2, x, y):
  return Motte(motte1.randomAllel().mutate(), motte2.randomAllel().mutate(), x, y, 0)
