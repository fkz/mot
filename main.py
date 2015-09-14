#!/usr/bin/env python

import random
import pygame
import sys

from environment import Environment

if __name__ == "__main__":
  pygame.init()
  env = Environment(10,10)
  env.generateRandom(20)
  screen = pygame.display.set_mode((1000,1000))
  env.draw(screen)
  pygame.display.update()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit(); sys.exit();
