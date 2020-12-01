# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 08:55:22 2020

@author: Mark Ferguson
"""

from itertools import combinations

with open('inputs/input1.txt') as fh:
  values = fh.readlines()

vals = [int(value.strip("\n")) for value in values]

# Part 1
for val1, val2 in combinations(vals, 2):
  if val1 + val2 == 2020:
    print(val1*val2)

# Part 2
for val1, val2, val3 in combinations(vals, 3):
  if val1 + val2 + val3 == 2020:
    print(val1*val2*val3)
