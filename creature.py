
import random

class Creature(object):  
  def __init__(self, x, y):
    self.x = x
    self.y = y
  """
  returns a list of actions
  """
  def step(self):
    pass
  
  def doMove(self):
    dx = 0; dy = 0;
    direction = random.randint(0, 3)
    if direction == 0: # try up
      dy = -1
    elif direction == 1: # try down
      dy = 1
    elif direction == 2: # try left
      dx = -1
    elif direction == 3: # try right
      dx = +1
    else:
      assert True, "random is wrong"
    return MoveCreature(dx, dy)

class Action:
  """
  an action is an interaction of a mot with the environment
  """
  def executeAction(self, mot, environment):
    assert True, "This is an abstract action"

class MoveCreature(Action):
  """
  move in some direction if possible
  """
  def __init__(self, dx, dy):
    self.dx = dx
    self.dy = dy
  def executeAction(self, creature, environment):
    environment.move(creature, self.dx, self.dy)
  def __str__(self):
    return "move by dx={0} dy={1}".format(self.dx, self.dy)
