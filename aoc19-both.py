# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 11:53:28 2020

@author: Mark Ferguson
"""
import re
from tokenize import tokenize, OP, NUMBER, STRING, NAME
from collections import defaultdict
from functools import reduce

with open('inputs/input19.txt', mode='rb') as fh:
  data = list(tokenize(fh.readline))

rule_input = defaultdict(list)
to_check = []
parse = {
  NUMBER: lambda x: int(x),
  OP: lambda x: x,
  STRING: lambda x: x.replace('"', ''),
  NAME: lambda x: to_check.append(x)
}

for token in data:
  if token.type in parse:
    val = parse[token.type](token.string)
    if val is not None:
      rule_input[token.start[0]].append(val)

rules = {rule[0]:rule[2:] for rule in rule_input.values()}

def concat(a, b): return str(a) + str(b)

def get_alternatives(rule):
  alts = []
  remainder = rule.copy()
  while True:
    try:
      or_ = remainder.index('|')
    except ValueError:
      alts.append(remainder)
      break
    alts.append(remainder[:or_])
    remainder = remainder[(or_ + 1):]
  return alts  
    
def no_alts(rule):
  return reduce(concat, [pattern(ix, rules) for ix in rule])  

def my_join(lst):
  ret = ''
  for sub_list in lst:
    ret += no_alts(sub_list)
    ret += '|'
  return ret[:-1]

def pattern(idx, rules):
  if rules[idx][0] == 'a':
    return 'a'
  if rules[idx][0] == 'b':
    return 'b'
  try:
    or_ = rules[idx].index('|')
  except ValueError:
    return no_alts(rules[idx])
  return reduce(
    concat,
    [
      '(?:',
      my_join(get_alternatives(rules[idx])),
      ')'
    ],
    )

tot = 0
matcher = re.compile(pattern(0, rules))
for string in to_check:
  match = matcher.match(string)
  if match:
    if match.group() == string:
      tot += 1
      
print(tot)

n = 5
rule8 = []
for i in range(1,n+1):
  rule8.extend([42]*i)
  if i < n:
    rule8.append('|')
rule11 = []
for i in range(1,n+1):
  rule11.extend([42]*i)
  rule11.extend([31]*i)
  if i < n:
    rule11.append('|')

rules[8] = rule8
rules[11] = rule11
tot = 0
matcher = re.compile(pattern(0, rules))
for string in to_check:
  match = matcher.match(string)
  if match:
    if match.group() == string:
      tot += 1
      
print(tot)


