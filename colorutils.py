#!/usr/bin/python

import math
import random

def randomRGB():
  return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def colorDistanceSingle(r1, g1, b1, r2, g2, b2): # returns value between 0 and 100
  (l1, a1, b1) = colorToLab(r1, g1, b1)
  (l2, a2, b2) = colorToLab(r2, g2, b2)
  return (math.sqrt((l1-l2)**2) + math.sqrt((a1-a2)**2) + math.sqrt((b1-b2)**2)) / 2.55

def colorDistance(rgb1, rgb2):
  return colorDistanceSingle(rgb1[0], rgb1[1], rgb1[2], rgb2[0], rgb2[1], rgb2[2])

def colorToLab(R, G, B):
  # http://www.brucelindbloom.com

  eps = 216.0 / 24389.0
  k = 24389.0 / 27.0

  Xr = 0.964221  # reference white D50
  Yr = 1.0
  Zr = 0.825211

  # RGB to XYZ
  r = R / 255.0 #R 0..1
  g = G / 255.0 #G 0..1
  b = B / 255.0 #B 0..1

  # assuming sRGB (D65)
  if (r <= 0.04045):
    r = r / 12;
  else:
    r = ((r + 0.055) / 1.055) ** 2.4

  if (g <= 0.04045):
    g = g / 12
  else:
    g = ((g + 0.055) / 1.055) ** 2.4
  if (b <= 0.04045):
    b = b / 12
  else:
    b = ((b + 0.055) / 1.055) ** 2.4

  X = 0.436052025 * r + 0.385081593 * g + 0.143087414 * b
  Y = 0.222491598 * r + 0.71688606 * g + 0.060621486 * b
  Z = 0.013929122 * r + 0.097097002 * g + 0.71418547 * b

  # XYZ to Lab
  xr = X / Xr
  yr = Y / Yr
  zr = Z / Zr

  if (xr > eps):
    fx = xr ** (1 / 3.0)
  else:
    fx = (k * xr + 16.0) / 116.0

  if (yr > eps):
    fy = yr ** (1 / 3.0)
  else:
    fy = (k * yr + 16.0) / 116.0

  if (zr > eps):
    fz = zr ** (1 / 3.0)
  else:
    fz = (k * zr + 16.0) / 116.0

  Ls = (116 * fy) - 16
  fas = 500 * (fx - fy)
  fbs = 200 * (fy - fz)

  l = int(2.55 * Ls + 0.5)
  a = int(fas + 0.5)
  b = int(fbs + 0.5)
  return (l, a, b)
