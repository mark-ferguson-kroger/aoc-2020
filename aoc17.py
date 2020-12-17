# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 23:55:57 2020

@author: Mark Ferguson
"""
import numpy as np
from time import time
t = time()

def to_num(line):
  return [
    int(char) for char 
    in line.replace("#", "1").replace(".", "0")
  ]

with open('inputs/input17.txt') as fh:
  data = np.array([to_num(line.strip()) for line in fh.readlines()], int)

data.shape = (1, data.shape[0], data.shape[1])

def grow_space(data):
  z, x, y = data.shape
  new_space = np.zeros((z + 2, x + 2, y + 2), int)
  new_space[1:(z+1), 1:(x+1), 1:(y+1)] = data.copy()
  return new_space

def valid(address, shape):
  az, ay, ax = address
  z, y, x = shape
  return (
    az >= 0 and az < z and
    ax >= 0 and ax < x and
    ay >= 0 and ay < y
  )

def living_neighbors(address, data):
  tot = 0
  az, ax, ay = address
  for z in (-1, 0, 1):
    for x in (-1, 0, 1):
      for y in (-1, 0, 1):
        if (z, x, y) == (0, 0, 0):
          pass
        else:
          new_z, new_x, new_y = az + z, ax + x, ay + y
          if valid((new_z, new_x, new_y), data.shape):
            tot += data[new_z, new_x, new_y]
  return tot

def count_em(data):
  count = np.zeros_like(data, int)
  Z, X, Y = data.shape
  for z in range(Z):
    for x in range(X):
      for y in range(Y):
        count[z, x, y] = living_neighbors((z,x,y), data)
  return count
  

def update_space(data):
  old_space = grow_space(data)
  new_space = np.zeros_like(old_space, int)
  Z, Y, X = new_space.shape
  for z in range(Z):
    for x in range(X):
      for y in range(Y):
        nabes = living_neighbors((z,x,y), old_space)
        if old_space[z, x, y] == 1:
          if nabes in (2,3):
            new_space[z, x, y] = 1
          else:
            new_space[z, x, y] = 0
        else:
          if nabes == 3:
            new_space[z, x, y] = 1
          else:
            new_space[z, x, y] = 0
  return new_space


for i in range(6):
  data = update_space(data)
  print(i, np.sum(data))

