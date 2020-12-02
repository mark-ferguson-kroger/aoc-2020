# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 08:27:54 2020

@author: Mark Ferguson
"""

import re
from collections import Counter

with open('inputs/input2.txt') as fh:
  lines = fh.readlines()

# 11-12 c: ccccgcccccpc
parser = re.compile(r'^(\d+)-(\d+) (\w): (\w+)$')

pwds = 0
for line in lines:
  parsed = re.search(parser, line)
  least, most, char, pwd = parsed.groups()  
  stats = Counter(pwd)
  if int(least) <= stats[char] <= int(most):
    pwds += 1

print(pwds)

pwds = 0
for line in lines:
  parsed = re.search(parser, line)
  first, second, char, pwd = parsed.groups()  
  occurrences = 0
  if pwd[int(first)-1] == char:
    occurrences += 1
  if pwd[int(second)-1] == char:
    occurrences += 1
  if occurrences == 1:
    pwds += 1

print(pwds)