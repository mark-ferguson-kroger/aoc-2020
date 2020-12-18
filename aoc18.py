# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 00:03:15 2020

@author: KON2763
"""
from re import split
from time import time
t = time()
with open('inputs/input18.txt') as fh:
  problems = [split(r'([\s\(\)])',line.strip()) for line in fh.readlines()]

for problem in problems:
  while True:
    try:
      problem.remove('')
    except ValueError:
      break
  while True:
    try:
      problem.remove(' ')
    except ValueError:
      break

ops = {
  '+': lambda x, y: x + y,
  '*': lambda x, y: x * y
}

def eval_chunk(chunk):
  left = int(chunk.pop(0))
  while chunk:
    op = chunk.pop(0)
    right = int(chunk.pop(0))
    left = ops[op](left, right)
  return left

def find_brackets(problem):
  opens = []
  pairs = []
  for i, glyph in enumerate(problem):
    if glyph == '(':
      opens.append(i)
    elif glyph == ')':
      pairs.append((opens.pop(), i))
  if pairs:
    return pairs.pop(0)

def parse_problem(problem):
  while True:
    idx = find_brackets(problem)
    if idx:
      problem = (
        problem[:idx[0]] + 
        [eval_chunk(problem[(idx[0]+1):idx[1]])] + 
        problem[(idx[1]+1):]
        )
    else:
      break
  return eval_chunk(problem)

acc = 0
for problem in problems:
  acc += parse_problem(problem)
  
print(acc)
print(time() - t)