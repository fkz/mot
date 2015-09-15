#!/usr/bin/env python

import random
import pygame
import sys

from environment import Environment

def drawGameOverScreen(screen):
  screen.fill((0,0,0))
  myfont = pygame.font.SysFont("monospace", 15)
  label = myfont.render("All mots are dead!", 1, (255,255,0))
  screen.blit(label, (100, 100))
  pygame.display.update()

if __name__ == "__main__":
  pygame.init()
  env = Environment(30,30)
  env.generateRandom(100)
  screen = pygame.display.set_mode((1000,1000))
  env.draw(screen)
  pygame.display.update()
  #time = 0

  gameOver = False

  while True:
    #time += 1
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit(); sys.exit();
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and gameOver == False:
          env.step()
          env.draw(screen)
          if len(env.mots) == 0:
            gameOver = True
        if gameOver == True:
          drawGameOverScreen(screen)
          #time = 0
    #if time == 200000:
     #   env.step()
      #  env.draw(screen)
       # time = 0
