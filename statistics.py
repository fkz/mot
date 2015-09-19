
  """
  do some additional work in specific actions like mating etc.
  can be used to generate cumulative statistics or show some additional info
  """
class Statistics:
  """
  is called every time an action has been executed
  """
  def mergeAction(self, environment, creature, action):
    pass
  """
  is called every time a new generational step was made
  """
  def step(self):
    pass
  """
  can output some additional info which is shown in the simulation
  """
  def info(self):
    return None
