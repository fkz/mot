from statistics import Statistics
from motte import PairWith, MotDies, Motte
from eagle import KillEagle


class MotsAlive(Statistics):
  def __init__(self, env):
    self.mots = {}
    for pos in env.allCellPositions():
      mot = env.cells[pos][Motte]
      if mot != None:
        self.mots[mot] = True
        self.addMot(mot, env)
  def step(self, env):
    pass
  def mergeAction(self, env, creature, action):
    if isinstance(action, MotDies):
      self.removeMot(creature, env)
    if isinstance(action, KillEagle):
      self.removeMot(action.killedMot, env)
    if isinstance(action, PairWith):
      self.addMot(action.child, env)
  def addMot(self, mot, env):
    pass
  def removeMot(self, mot, env):
    pass
