# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 23:55:25 2020

@author: Mark Ferguson
"""
import re
from functools import reduce
rule_re = re.compile(r'([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)')
with open('inputs/input16.txt') as fh:
  rules = {}
  mine = None
  tix = []
  mine_next = False
  tix_next = False
  for line in fh.readlines():
    if mine_next:
      mine = [int(x) for x in line.strip().split(',')]
      mine_next = False
    elif tix_next:
      tix.append([
        int(x) for x in line.strip().split(',')
      ])
    elif re.match('your ticket:', line):
      mine_next = True
    elif re.match('nearby tickets:', line):
      tix_next = True
    elif rule_re.match(line):
      rule, a, b, c, d = rule_re.match(line).groups()
      rules[rule] = (int(a), int(b), int(c), int(d))

def make_tester(rules):
  tester = {}
  for rule, ranges in rules.items():
    a,b,c,d = ranges
    tester[rule] = lambda x, a=a, b=b, c=c, d=d: (a <= x <= b) or (c <= x <= d)
  return tester

def test_ticket(ticket, tester):
  bad = []
  for val in ticket:
    good = reduce(
      lambda x, y: x or y,
      [test(val) for test in tester.values()]
    )
    if not good:
      bad.append(val)
  return sum(bad)

tester = make_tester(rules)
print(sum([test_ticket(ticket, tester) for ticket in tix]))

valid = [ticket for ticket in tix if test_ticket(ticket, tester) == 0]
valid.append(mine)

n = len(valid[0])
mapping = {rule:[] for rule in tester}
for rule, test in tester.items():
  for slot in range(n):
    good = reduce(
      lambda x, y: x and y,
      [test(ticket[slot]) for ticket in valid]
    )
    if good:
      mapping[rule].append(slot)

# Collapse rules
lens = {len(slots):rule for rule, slots in mapping.items()}  

for length in range(1, n):
  value = mapping[lens[length]][0]
  for longer in range(length + 1, n):
    mapping[lens[longer]].remove(value)

tot = 1
for rule, slot in mapping.items():
  print(rule, slot[0])
  if re.match('departure', rule):
    print('y')
    tot *= mine[slot[0]]
    
print(tot)