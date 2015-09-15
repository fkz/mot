
class Creature(object):  
  def __init__(self, x, y):
    self.x = x
    self.y = y
  """
  returns a list of actions
  """
  def step(self):
    pass

class Action:
  """
  an action is an interaction of a mot with the environment
  """
  def executeAction(self, mot, environment):
    assert True, "This is an abstract action"
