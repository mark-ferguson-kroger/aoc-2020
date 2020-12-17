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

data.shape = (1, 1, data.shape[0], data.shape[1])

def living_neighbors(address, data):
  W, Z, X, Y = data.shape
  aw, az, ax, ay = address
  neighbors = data[
    max((aw-1), 0):min((aw+2), W),
    max((az-1), 0):min((az+2), Z),
    max((ax-1), 0):min((ax+2), X),
    max((ay-1), 0):min((ay+2), Y),
  ]
  return np.sum(neighbors) - data[aw, az, ax, ay]

def count_em(data):
  count = np.zeros_like(data, int)
  W, Z, X, Y = data.shape
  for w in range(W):
    for z in range(Z):
      for x in range(X):
        for y in range(Y):
          count[w, z, x, y] = living_neighbors((w, z,x,y), data)
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
  W, Z, X, Y = new_space.shape
  boundary = np.array([[W, 0],[Z, 0],[X, 0],[Y, 0]])
  nabes = count_em(old_space)
  for w in range(W):
    for z in range(Z):
      for x in range(X):
        for y in range(Y):
          if old_space[w, z, x, y] == 1:
            if nabes[w, z, x, y] in (2,3):
              new_space[w, z, x, y] = 1
              boundaries((w,z,x,y), boundary)
            else:
              new_space[w, z, x, y] = 0
          else:
            if nabes[w, z, x, y] == 3:
              new_space[w, z, x, y] = 1
              boundaries((w,z,x,y), boundary)
            else:
              new_space[w, z, x, y] = 0
  w, z, x, y = boundary[0], boundary[1], boundary[2], boundary[3]
  return new_space[w[0]:(w[1]+1), z[0]:(z[1]+1), x[0]:(x[1]+1), y[0]:(y[1]+1)]


for i in range(6):
  data = update_space(data)
  print(i, np.sum(data))

print(time()-t)
