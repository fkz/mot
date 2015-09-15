#!/usr/bin/env python

import random
import pygame
import sys

from environment import Environment

timePerStepInMilliseconds = 100

def drawGameOverScreen(screen):
  screen.fill((0,0,0))
  myimage = pygame.image.load("tote_motte.jpg")
  imagerect = myimage.get_rect()
  screen.blit(myimage, imagerect)
  myfont = pygame.font.SysFont("monospace", 15)
  label = myfont.render("All mots are dead!", 1, (255,255,0))
  screen.blit(label, (100, 100))
  pygame.display.update()

if __name__ == "__main__":
  pygame.init()
  env = Environment(30,30)
  env.generateRandom(100)
  screen = pygame.display.set_mode((800,800))
  env.draw(screen)
  pygame.display.update()

  gameOver = False
  while True:
    currentTime = pygame.time.get_ticks()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit(); sys.exit();
    env.step()
    env.draw(screen)
    if len(env.mots) == 0:
      gameOver = True
      if gameOver == True:
        drawGameOverScreen(screen)
    pygame.time.wait (timePerStepInMilliseconds - (pygame.time.get_ticks() - currentTime))
