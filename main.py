#!/usr/bin/env python

import random
import pygame
import sys

from environment import Environment
from visuals import Visuals

timePerStepInMilliseconds = 20

if __name__ == "__main__":
  pygame.init()
  screen = pygame.display.set_mode((800,800))
  env = Environment(5,5)
  env.generateRandom(5000)
  env.makeStripeColors()
  visuals = Visuals(screen, env)
  visuals.drawField()

  gameOver = False
  while True:
    currentTime = pygame.time.get_ticks()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit(); sys.exit();
    if not gameOver:
      env.step()
      visuals.drawField()
    if env.numMots == 0:
      gameOver = True
      visuals.drawGameOverScreen()
    pygame.time.wait (timePerStepInMilliseconds - (pygame.time.get_ticks() - currentTime))

  
