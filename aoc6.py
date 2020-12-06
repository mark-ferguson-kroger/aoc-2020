# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 23:58:58 2020

@author: Mark Ferguson
"""

from collections import Counter

with open('inputs/input6.txt') as fh:
  lines = [line.strip() for line in fh.readlines()]
 
# Simplify group algo
lines.append('')

group = ''
nums = []
for line in lines:
  if line == '':
    nums.append(len(Counter(group)))
    group = ''
  else:
    group += line
    
print(sum(nums))

def check(counter, size):
  tot = 0
  for answer, num in counter.items():
    if num == size:
      tot += 1
  return tot

group = ''
nums = []
size = 0
for line in lines:
  if line == '':
    nums.append(check(Counter(group), size))
    group = ''
    size = 0
  else:
    size += 1
    group += line
    
print(sum(nums))
