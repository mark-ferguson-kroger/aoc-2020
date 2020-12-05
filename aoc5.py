# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 23:56:58 2020

@author: Mark Ferguson
"""
with open('inputs/input5.txt') as fh:
  lines = [line.strip() for line in fh.readlines()]
  
def num(spec):
  bi = (
    spec
    .replace('B', '1')
    .replace('F', '0')
    .replace('R', '1')
    .replace('L', '0')
  )
  return int(bi, 2)

plane = [num(line) for line in lines]
print(max(plane))

# All seats
comp = set(list(range(min(plane), max(plane) + 1)))

# My seat
print(comp.symmetric_difference(set(plane)))
