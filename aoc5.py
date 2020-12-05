# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 23:56:58 2020

@author: Mark Ferguson
"""
from pandas import DataFrame

with open('inputs/input5.txt') as fh:
  lines = [line.strip() for line in fh.readlines()]
  
def num(spec):
  bi = spec[:7].replace('B', '1').replace('F', '0')
  row = int(bi, 2)

  bi = spec[-3:].replace('R', '1').replace('L', '0')
  col = int(bi, 2)

  seat = 8 * row + col
  
  return seat, row, col


plane = [num(line) for line in lines]

foo = DataFrame(data=plane, columns=['seat', 'row', 'col'])
print(max(foo['seat']))

# filled seats
filled = set(list(foo['seat'].values))

# All seats
comp = set(list(range(min(foo['seat']),max(foo['seat'])+1)))

# My seat
print(filled.symmetric_difference(comp))
