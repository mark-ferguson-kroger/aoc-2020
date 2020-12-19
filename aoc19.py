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

def pattern(idx, rules):
  if rules[idx][0] == 'a':
    return 'a'
  if rules[idx][0] == 'b':
    return 'b'
  try:
    or_ = rules[idx].index('|')
  except ValueError:
    return reduce(concat, [pattern(ix, rules) for ix in rules[idx]])
  return reduce(
    concat,
    [
      '(?:', 
      reduce(concat, [pattern(ix, rules) for ix in rules[idx][:or_]]), 
      '|', 
      reduce(concat, [pattern(idx, rules) for idx in rules[idx][(or_ + 1):]]),
      ')'
    ],
    )

matcher = re.compile(pattern(0, rules))

tot = 0
for string in to_check:
  match = matcher.match(string)
  if match:
    if match.group() == string:
      tot += 1
      
print(tot)
  
