#!/usr/bin/env python

import pygame

from settings import minMatingAge

class Visuals:
  def __init__(self, screen, env):
    self.screen = screen
    self.env = env
    screenWidth = screen.get_width()
    screenHeight = screen.get_height()
    envWidth = env.width
    envHeight = env.height
    cellDim = max(envWidth, envHeight)
    screenDim = min(screenWidth, screenHeight)
    self.length = screenDim / (cellDim)
    self.adlerImage = pygame.image.load("adler.png").convert_alpha()
    self.adlerImage = pygame.transform.scale(self.adlerImage, (self.length, self.length))

  def drawField(self):
    screen = self.screen
    length = self.length
    for x in range(0, self.env.width):
      for y in range(0, self.env.height):
        pygame.draw.rect(screen, (0,0,0), (x * length-1, y * length-1, length+2, length+2), 0)
        cell = self.env.cells[x,y]

        pygame.draw.rect(screen, cell.color, (x * length, y * length, length, length), 0)
        if cell.mot != None:
          color = cell.mot.color
          ripeness = min(float(cell.mot.age) / float(minMatingAge), 1.0)
          adultRadius = length/2
          myRadius = max(int(ripeness * adultRadius), 4)
          pygame.draw.circle(screen, (0,0,0), (x * length + length/2, y*length + length/2), myRadius, 0)
          pygame.draw.circle(screen, color, (x * length + length/2, y*length + length/2), myRadius -1, 0)

          allelRadius = max(int(myRadius / 2) - 1, 1)
          color1 = cell.mot.allel1.rgb
          color2 = cell.mot.allel2.rgb
          pygame.draw.circle(screen, color1, (x * length + length/2 - allelRadius, y*length + length/2), allelRadius, 0)
          pygame.draw.circle(screen, color2, (x * length + length/2 + allelRadius, y*length + length/2), allelRadius, 0)
        screen.blit(self.adlerImage, pygame.rect.Rect(x * length, y * length, length, length))
    pygame.display.update()

  def drawGameOverScreen(self):
    screen = self.screen
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
