#!/usr/bin/env python

import pygame
import argparse
import itertools
import pdb

from environment import Environment
from visuals import Visuals, Visual
from TreeStatistics import TreeStatistics
from allactions import AllActions
from difference import Difference, DifferenceGraph

timePerStepInMilliseconds = 20

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Simulate mots')
  parser.add_argument('--height', type=int, default=20,
                   help='the height of the grid')
  parser.add_argument('--width', type=int, default=20,
                   help='the width of the grid')
  parser.add_argument('--motcount', type=int, default=100, help="The number of mots which are spawned at begin")
  parser.add_argument('--speed', type=int, default=0, help="Number of milliseconds between two steps")
  parser.add_argument('--draw', action='store_true', help='make a graphical simulation')
  parser.add_argument('--tree', help='make a dot graph at the position')
  parser.add_argument('--rounds', type=int, help='number of rounds', default=0)
  parser.add_argument('--printactions', action='store_true', help='Print actions')
  parser.add_argument('--difference', action='store_true', help='Show difference')
  parser.add_argument('--differenceo', help='difference output')

  args = parser.parse_args()
  
  env = Environment(args.height, args.width)
  env.generateRandom(args.motcount)

  statistics = []
  
  if args.draw:
    visual = Visual(env)
  else:
    visual = None
    
  if args.tree:
    statistics.append(TreeStatistics(env, args.tree))
  
  if args.printactions:
    statistics.append(AllActions())
  
  if args.difference:
    statistics.append(Difference(env))
  
  if args.differenceo:
    statistics.append(DifferenceGraph(env, args.differenceo))
  
  for s in statistics:
    s.__enter__()

  try:
    if args.rounds > 0:
      it = range(args.rounds)
    else:
      it = itertools.repeat(0)
    for rounds in it:
      if visual:
        currentTime = pygame.time.get_ticks()
      for s in statistics:
        s.step(env)
      if visual:
        infos = map(lambda x: x.info(), statistics)
        visual.step(env, infos)
      for creature, action in env.stepWithAge():
        for s in statistics:
          s.mergeAction(env, creature, action)
      if visual:
        pygame.time.wait (args.speed - (pygame.time.get_ticks() - currentTime))
  finally:
    for s in statistics:
      s.__exit__()
