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

def living_neighbors(address, data):
  Z, X, Y = data.shape
  az, ax, ay = address
  neighbors = data[
    max((az-1), 0):min((az+2), Z),
    max((ax-1), 0):min((ax+2), X),
    max((ay-1), 0):min((ay+2), Y),
  ]
  return np.sum(neighbors) - data[az, ax, ay]

def count_em(data):
  count = np.zeros_like(data, int)
  Z, X, Y = data.shape
  for z in range(Z):
    for x in range(X):
      for y in range(Y):
        count[z, x, y] = living_neighbors((z,x,y), data)
  return count
  
def boundaries(address, boundary):
  for dim in range(len(boundary)):
    if address[dim] < boundary[dim, 0]:
      boundary[dim, 0] = address[dim]
    if address[dim] > boundary[dim, 1]:
      boundary[dim, 1] = address[dim]
  return boundary

def update_space(data):
  old_space = np.pad(data, pad_width=1, mode='constant', constant_values=0)
  new_space = np.zeros_like(old_space, int)
  Z, X, Y = new_space.shape
  boundary = np.array([[Z, 0],[X, 0],[Y, 0]])
  nabes = count_em(old_space)
  for z in range(Z):
    for x in range(X):
      for y in range(Y):
        if old_space[z, x, y] == 1:
          if nabes[z, x, y] in (2,3):
            new_space[z, x, y] = 1
            boundaries((z,x,y), boundary)
          else:
            new_space[z, x, y] = 0
        else:
          if nabes[z, x, y] == 3:
            new_space[z, x, y] = 1
            boundaries((z,x,y), boundary)
          else:
            new_space[z, x, y] = 0
  z, x, y = boundary[0], boundary[1], boundary[2]
  return new_space[z[0]:(z[1]+1), x[0]:(x[1]+1), y[0]:(y[1]+1)]


for i in range(6):
  data = update_space(data)
  print(i, np.sum(data))

print(time()-t)
