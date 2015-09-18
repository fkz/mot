from statistics import Statistics

class AllActions(Statistics):
  round = 0
  def mergeAction(self, env, creature, action):
    print action
  def step(self, env):
    ++self.round
    print "Round {}".format(self.round)
  def __enter__(self):
    pass
  def __exit__(self):
    pass
