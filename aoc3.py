# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 23:59:29 2020

@author: Mark Ferguson
"""

with open('inputs/input3.txt') as fh:
  lines = fh.readlines()

text = [line.strip() for line in lines]

def traverse(text, right, down):
  rows = len(text)
  columns = len(text[0])
  row = 0
  col = 0
  trees = 0
  while row < (rows - 1):
    row, col = row + down, (col + right) % columns
    try:
      if text[row][col] == '#':
        trees += 1
    except:
      pass
  return trees

trees = traverse(text, 3, 1)

print(trees)

# Right 1, down 1.
# Right 3, down 1.
# Right 5, down 1.
# Right 7, down 1.
# Right 1, down 2.

toboggans = (
  (1, 1),
  (3, 1),
  (5, 1),
  (7, 1),
  (1, 2)
)

trees = []
for right, down in toboggans:
  trees.append(traverse(text, right, down))
  
total = 1
for tree_num in trees:
  total *= tree_num
  
print(total)