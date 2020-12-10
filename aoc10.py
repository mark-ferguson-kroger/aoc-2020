# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 07:42:13 2020

@author: Mark Ferguson
"""
from collections import Counter

with open('inputs/input10.txt') as fh:
  data = [int(line.strip()) for line in fh.readlines()]

rating = max(data) + 3

data = [0] + sorted(data)
data.append(rating)

diffs = [x - data[idx] for idx, x in enumerate(data[1:])]

count = Counter(diffs)

print(count)
print(count[1] * count[3])

runs = []
foo = iter(diffs)
while True:
  count = 0
  try:
    while foo.__next__() == 1:
      count += 1
  except StopIteration:
    break
  if count > 0:
    runs.append(count)
print(runs)  

mult = {
  1:1,
  2:2,
  3:4,
  4:7
}

tot = 1
for run in runs:
  tot *= mult[run]

print(tot)