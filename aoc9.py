# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 23:59:29 2020

@author: Mark Ferguson
"""
from itertools import combinations
with open('inputs/input9.txt') as fh:
  data = [int(line.strip()) for line in fh.readlines()]
window = 25
def test(val, chunk):
  for x, y in combinations(chunk, 2):
    if val == x + y:
      return True
  return False

def legal(data, window):
  n = len(data)
  for start in range(window, n):
    if not test(data[start], data[(start - window):start]):
      return data[start]
    
  return None

key = legal(data, window)
print(key)

def weakness(data, key):
  for first, last in combinations(range(len(data)), 2):
    chunk = data[first:last]
    if sum(chunk) == key:
      return max(chunk) + min(chunk)
    
  return None

print(weakness(data, key))