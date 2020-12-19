# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 11:53:28 2020

@author: Mark Ferguson
"""
import re
from tokenize import tokenize, OP, NUMBER, STRING, NAME
from collections import defaultdict
from functools import reduce
from time import time
t = time()
with open('inputs/input19.txt', mode='rb') as fh:
  data = list(tokenize(fh.readline))

rule_input = defaultdict(list)
to_check = []
for token in data:
  if token.type == NUMBER:
    val = int(token.string)
  elif token.type == OP:
    val = token.string
  elif token.type == STRING:
    val = token.string.replace('"', '')
  elif token.type == NAME:
    to_check.append(token.string)
    continue
  else:
    continue
  rule_input[token.start[0]].append(val)

rules = {rule[0]:rule[2:] for rule in rule_input.values()}

def concat(a, b): return str(a) + str(b)

def pattern(idx, rules, n):
  if rules[idx][0] == 'a':
    return 'a'
  if rules[idx][0] == 'b':
    return 'b'
  if idx == 8:
    # 8: 42 | 42 8
    p42 = pattern(42, rules, n)
    middle = []
    for i in range(1,n+1):
      middle.extend([p42]*i)
      if i < n:
        middle.append('|')
    return reduce(concat, ['(?:'] + middle + [')'])
  if idx == 11:
    # 11: 42 31 | 42 11 31
    p42 = pattern(42, rules, n)
    p31 = pattern(31, rules, n)
    middle = []
    for i in range(1,n+1):
      middle.extend([p42]*i)
      middle.extend([p31]*i)
      if i < n:
        middle.append('|')
    return reduce(concat, ['(?:'] + middle + [')'])
  try:
    or_ = rules[idx].index('|')
  except ValueError:
    return reduce(concat, [pattern(ix, rules, n) for ix in rules[idx]])
  return reduce(
  concat,
  [
    '(?:', 
    reduce(concat, [pattern(ix, rules, n) for ix in rules[idx][:or_]]), 
    '|', 
    reduce(concat, [pattern(idx, rules, n) for idx in rules[idx][(or_ + 1):]]),
    ')'
  ],
  )
  
pat = pattern(0, rules, 10)
print(len(pat))
matcher = re.compile(pat)

tot = 0
for string in to_check:
  match = matcher.match(string)
  if match:
    if match.group() == string:
      tot += 1
    
print(tot)

