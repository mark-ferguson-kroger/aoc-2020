# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 00:03:15 2020

@author: KON2763
"""
from tokenize import tokenize, OP, NUMBER
from collections import defaultdict
from copy import deepcopy
from time import time
t = time()
with open('inputs/input18.txt', mode='rb') as fh:
  data = list(tokenize(fh.readline))

problems = defaultdict(list)
for token in data:
  if token.type == NUMBER:
    val = int(token.string)
  elif token.type == OP:
    val = token.string
  else:
    continue
  problems[token.start[0]].append(val)
   
ops = {
  '+': lambda x, y: x + y,
  '*': lambda x, y: x * y
}

def eval_chunk(chunk):
  left = chunk.pop(0)
  while chunk:
    op = chunk.pop(0)
    right = chunk.pop(0)
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
for _, problem in deepcopy(problems).items():
  acc += parse_problem(problem)
  
print(acc)
print(time() - t)
t = time()

def eval_ordered(chunk):
  while True:
    try:
      plus = chunk.index('+')
    except ValueError:
      break
    chunk = (
      chunk[:(plus-1)] + 
      [chunk[plus-1] + chunk[plus+1]] +
      chunk[(plus+2):]
    )
  return eval_chunk(chunk)

def parse_ordered(problem):
  while True:
    idx = find_brackets(problem)
    if idx:
      problem = (
        problem[:idx[0]] + 
        [eval_ordered(problem[(idx[0]+1):idx[1]])] + 
        problem[(idx[1]+1):]
        )
    else:
      break
  return eval_ordered(problem)

acc = 0
for _, problem in deepcopy(problems).items():
  val = parse_ordered(problem)
  acc += val
  
print(acc)
print(time() - t)
