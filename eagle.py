
import random

from creature import Creature, Action
from colorutils import colorDistance
from settings import enemyVision
from motte import Motte

class Eagle(Creature):
  def __init__(self, x, y):
    super(Eagle, self).__init__(x, y)
  def shouldKillEagle(self, environment):
    mot = environment.cells[self.x,self.y][Motte]
    if mot == None:
      return False
    fitness = (colorDistance(environment.cells[self.x,self.y].color, mot.color))
    isDying = random.randint(0,100)
    if isDying < int(fitness * enemyVision):
      return True

  def step(self, environment):
    if self.shouldKillEagle(environment):
      yield KillEagle()
    yield self.doMove()

class KillEagle(Action):
  def executeAction(self, eagle, environment):
    self.killedMot = environment.cells[eagle.x, eagle.y][Motte]
    environment.removeMot(self.killedMot)
