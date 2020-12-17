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

def active_neighbors(address, data):
  W, Z, X, Y = data.shape
  w, z, x, y = address
  cube = data[
    max((w-1), 0):min((w+2), W),
    max((z-1), 0):min((z+2), Z),
    max((x-1), 0):min((x+2), X),
    max((y-1), 0):min((y+2), Y),
  ]
  return np.sum(cube) - data[address]

def count_em(data):
  count = np.zeros_like(data, int)
  for address in np.ndindex(*data.shape):
          count[address] = active_neighbors(address, data)
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
  for address in np.ndindex(*old_space.shape):
    if old_space[address] == 1:
      if nabes[address] in (2,3):
        new_space[address] = 1
        boundary = boundaries(address, boundary)
      else:
        new_space[address] = 0
    else:
      if nabes[address] == 3:
        new_space[address] = 1
        boundary = boundaries(address, boundary)
      else:
        new_space[address] = 0
  w, z, x, y = boundary[0], boundary[1], boundary[2], boundary[3]
  return new_space[w[0]:(w[1]+1), z[0]:(z[1]+1), x[0]:(x[1]+1), y[0]:(y[1]+1)]


for i in range(6):
  data = update_space(data)
  print(i, np.sum(data))

print(time()-t)
