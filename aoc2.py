# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 08:27:54 2020

@author: Mark Ferguson
"""

from re import compile

with open('inputs/input2.txt') as fh:
  lines = fh.readlines()

# 11-12 c: ccccgcccccpc
parser = compile(r'^(\d+)-(\d+) (\w): (\w+)$')

pwds = 0
for line in lines:
  parsed = parser.search(line)
  least, most, char, pwd = parsed.groups()  
  if int(least) <= pwd.count(char) <= int(most):
    pwds += 1

print(pwds)

pwds = 0
for line in lines:
  parsed = parser.search(line)
  first, second, char, pwd = parsed.groups()  
  occurrences = 0
  if pwd[int(first)-1] == char:
    occurrences += 1
  if pwd[int(second)-1] == char:
    occurrences += 1
  if occurrences == 1:
    pwds += 1

print(pwds)