#!/usr/bin/env python

import random
import pygame
import sys

from environment import Environment
from visuals import Visuals
from colorutils import randomRGB

timePerStepInMilliseconds = 20

if __name__ == "__main__":
  pygame.init()
  infoObject = pygame.display.Info()
  screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
  env = Environment(200,200)
  env.generateRandom(1000)
  env.makeStripeColors(randomRGB(), randomRGB())
  visuals = Visuals(screen, env)
  visuals.drawField()

  gameOver = False
  while True:
    currentTime = pygame.time.get_ticks()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit(); sys.exit();
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          visuals.toggleXRay()
        if event.key == pygame.K_RETURN:
          env.makeStripeColors(randomRGB(), randomRGB())
        if event.key == pygame.K_LSHIFT:
          visuals.toggleShowEagles()
        if event.key == pygame.K_ESCAPE:
          pygame.quit(); sys.exit();
    if not gameOver:
      env.step()
      visuals.drawField()
    if env.numMots == 0:
      gameOver = True
      visuals.drawGameOverScreen()
    pygame.time.wait (timePerStepInMilliseconds - (pygame.time.get_ticks() - currentTime))
