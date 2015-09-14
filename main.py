#!/usr/bin/env python

import random
import pygame
import sys

from environment import Environment

if __name__ == "__main__":
  pygame.init()
  env = Environment(50,50)
  env.generateRandom(42)
  screen = pygame.display.set_mode((1000,1000))
  env.draw(screen)
  pygame.display.update()
  #time = 0

  while True:
    #time += 1
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit(); sys.exit();
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          env.step()
          env.draw(screen)
          #time = 0
    #if time == 200000:
     #   env.step()
      #  env.draw(screen)
       # time = 0
