# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 21:20:58 2020

@author: Mark Ferguson
"""
with open('inputs/input5.txt') as fh:
  plane = [int(line.strip().replace('B','1').replace('F','0').replace('R','1').replace('L','0'),2) for line in fh.readlines()]
print(max(plane))
# All seats
comp = set(list(range(min(plane), max(plane) + 1)))
# My seat
print(comp.symmetric_difference(set(plane)))
