#!/usr/bin/env python

import pygame

import sys
from settings import minMatingAge
from motte import Motte
from eagle import Eagle
from statistics import Statistics
from colorutils import randomRGB

class Visuals:
  def __init__(self, screen, env):
    self.screen = screen
    screenWidth = screen.get_width()
    screenHeight = screen.get_height()
    envWidth = env.width
    envHeight = env.height
    cellDim = max(envWidth, envHeight)
    screenDim = min(screenWidth, screenHeight)
    self.length = screenDim / (cellDim)
    self.adlerImage = pygame.image.load("adler.png").convert_alpha()
    self.adlerImage = pygame.transform.scale(self.adlerImage, (self.length, self.length))
    self.xray = True
    self.showEagles = True

  def drawInfoScreen(self, env):
    fontSize = 25
    fontSpacing = 2 * fontSize
    myfont = pygame.font.SysFont("monospace", fontSize)
    label = myfont.render("Toggle X-ray vision: SPACE", 1, (255,255,0))
    self.screen.blit(label, (env.width * self.length + 20, 10))
    label = myfont.render("Random Stripes: RETURN", 1, (255,255,0))
    self.screen.blit(label, (env.width * self.length + 20, 10 + fontSpacing))
    label = myfont.render("Toggle stealth Eagles: LSHIFT", 1, (255,255,0))
    self.screen.blit(label, (env.width * self.length + 20, 10 + fontSpacing * 2))
    label = myfont.render("Quit program: ESCAPE", 1, (255,255,0))
    self.screen.blit(label, (env.width * self.length + 20, 10 + fontSpacing * 3))
    pygame.display.update()

  def drawInfos(self, infos, env):
    fontSize = 25
    fontSpacing = 2 * fontSize
    myfont = pygame.font.SysFont("monospace", fontSize)
    height = 4
    for info in infos:
      ++height
      label = myfont.render(info, 1, (255, 255, 0))
      self.screen.fill((0, 0, 0), pygame.Rect(env.width * self.length + 20, 10 + fontSpacing * height, 2000, fontSpacing * height))
      self.screen.blit(label, (env.width * self.length + 20, 10 + fontSpacing * height))

  def drawField(self, env):
    screen = self.screen
    length = self.length
    for x in range(0, env.width):
      for y in range(0, env.height):
        cell = env.cells[x,y]
        updated = cell.updated
        if self.xray:
          updated = updated or cell.updatedEagle

        if updated:
          pygame.draw.rect(screen, cell.color, (x * length+1, y * length+1, length-1, length-1), 0)
          if cell[Motte] != None:
            color = cell[Motte].color
            ripeness = min(float(cell[Motte].age) / float(minMatingAge), 1.0)
            adultRadius = length/2
            myRadius = max(int(ripeness * adultRadius), 1)
            pygame.draw.circle(screen, (0,0,0), (x * length + length/2, y*length + length/2), myRadius, 0)
            pygame.draw.circle(screen, color, (x * length + length/2, y*length + length/2), myRadius -1, 0)

            if self.xray:
              allelRadius = max(int(myRadius / 2) - 1, 1)
              color1 = cell[Motte].allel1.rgb
              color2 = cell[Motte].allel2.rgb
              pygame.draw.circle(screen, color1, (x * length + length/2 - allelRadius, y*length + length/2), allelRadius, 0)
              pygame.draw.circle(screen, color2, (x * length + length/2 + allelRadius, y*length + length/2), allelRadius, 0)
          if self.showEagles and cell[Eagle] != None:
            screen.blit(self.adlerImage, pygame.rect.Rect(x * length, y * length, length, length))
          cell.updated = False
    self.drawInfoScreen(env)
    pygame.display.update()

  def toggleXRay(self, env):
    self.xray = not self.xray
    for x in range(0, env.width):
      for y in range(0, env.height):
        env.cells[x,y].updated = True

  def toggleShowEagles(self, env):
    self.showEagles = not self.showEagles
    for x in range(0, env.width):
      for y in range(0, env.height):
        env.cells[x,y].updated = True

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


class Visual(Statistics):
  def __init__(self, env):
    pygame.init()
    infoObject = pygame.display.Info()
    self.screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
    self.visuals = Visuals(self.screen, env)
    self.visuals.drawField(env)
  def __enter__(self):
    return self
  def __exit__(self):
    pass
  def step(self, env, infos):
    if env.numMots == 0:
      pygame.display.update()
      self.visuals.drawGameOverScreen()
    else:
      self.visuals.drawField(env)
      self.visuals.drawInfos(infos, env)
    first = True
    pause = False
    while first or pause:
      first = False
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit(); sys.exit();
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            self.visuals.toggleXRay(env)
          if event.key == pygame.K_RETURN:
            env.makeStripeColors(randomRGB(), randomRGB())
          if event.key == pygame.K_LSHIFT:
            self.visuals.toggleShowEagles(env)
          if event.key == pygame.K_ESCAPE:
            pygame.quit(); sys.exit();
          if event.key == pygame.K_l:
            pause = not pause
            pygame.time.wait(1000)
