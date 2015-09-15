
import random

from creature import Creature, Action
from colorutils import colorDistance
from settings import enemyVision


class Eagle(Creature):
  def __init__(self, x, y):
    super(Eagle, self).__init__(x, y)
  def step(self):
    return [KillEagle(), self.doMove()] * 4

class KillEagle(Action):
  def executeAction(self, eagle, environment):
    mot = environment.cells[eagle.x,eagle.y].mot
    if mot == None:
      return
    fitness = (colorDistance(environment.cells[eagle.x,eagle.y].color, mot.color))
    isDying = random.randint(0,100)
    if isDying < int(fitness * enemyVision):
      environment.removeMot(mot)

  
  
