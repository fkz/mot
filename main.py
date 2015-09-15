#!/usr/bin/env python

import random
import pygame
import sys

from environment import Environment

timePerStepInMilliseconds = 300

def drawGameOverScreen(screen):
  screen.fill((0,0,0))
  myimage = pygame.image.load("tote_motte.jpg")
  imagerect = myimage.get_rect()

  dx = screen.get_width() / 2 - imagerect.width / 2
  dy = screen.get_height() / 2 - imagerect.height / 2

  imagerect.move_ip(dx, dy)

  screen.blit(myimage, imagerect)
  myfont = pygame.font.SysFont("monospace", 25)
  label = myfont.render("All mots are dead!", 1, (255,255,0))
  screen.blit(label, (100, 100))
  pygame.display.update()

if __name__ == "__main__":
  pygame.init()
  env = Environment(40,40)
  env.generateRandom(2000)
  env.makeStripeColors()
  screen = pygame.display.set_mode((800,800))
  env.draw(screen)
  pygame.display.update()

  gameOver = False
  while True:
    currentTime = pygame.time.get_ticks()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit(); sys.exit();
    if not gameOver:
      env.step()
      env.draw(screen)
    if env.numMots == 0:
      gameOver = True
      drawGameOverScreen(screen)
    pygame.time.wait (timePerStepInMilliseconds - (pygame.time.get_ticks() - currentTime))

  
