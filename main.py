#!/usr/bin/env python

import random
import pygame
import sys
import argparse

from environment import Environment
from visuals import Visuals, Visual
from colorutils import randomRGB
from TreeStatistics import TreeStatistics

timePerStepInMilliseconds = 20

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Simulate mots')
  parser.add_argument('--height', type=int, default=20,
                   help='the height of the grid')
  parser.add_argument('--width', type=int, default=20,
                   help='the width of the grid')
  parser.add_argument('--motcount', type=int, default=100, help="The number of mots which are spawned at begin")
  parser.add_argument('--speed', type=int, default=100, help="Number of milliseconds between two steps")
  parser.add_argument('--draw', action='store_true', help='make a graphical simulation')
  parser.add_argument('--tree', help='make a dot graph at the position')

  args = parser.parse_args()
  
  env = Environment(args.width, args.height)
  env.generateRandom(args.motcount)

  statistics = []
  
  if args.draw:
    statistics.append(Visual(env))
  
  if args.tree:
    statistics.append(TreeStatistics(env, args.tree))
  
  for s in statistics:
    s.__enter__()

  try:
    while True:
      currentTime = pygame.time.get_ticks()
      for s in statistics:
        s.step(env)
      for creature, action in env.stepWithAge():
        for s in statistics:
          s.mergeAction(env, creature, action)
      pygame.time.wait (args.speed - (pygame.time.get_ticks() - currentTime))
  finally:
    for s in statistics:
      s.__exit__()
