# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 23:58:20 2020

@author: Mark Ferguson
"""
from re import compile
from functools import reduce

with open('inputs/input7.txt') as fh:
  lines = [line.strip() for line in fh.readlines()]

# Sub in zero for "no"
lines = [line.replace(' no ', ' 0 ') for line in lines]

owner = compile(r'(\w+ \w+) bags? contain')
held = compile(r'(\d+) (\w+ \w+) bag')

rules = {
  owner.match(line).groups()[0]:held.findall(line)
  for line in lines
}

def contain_gold(rule):
  contents = rules[rule]
  go_deeper = []
  for bag in contents:
    if 'shiny gold' in bag:
      return True
    else:
      go_deeper.append(bag[1])
  deeper = [contain_gold(rule) for rule in go_deeper]
  if deeper:
    return reduce(lambda x,y: x or y, deeper)
  else:
    return False
  
tot = 0
for rule in rules:
  if contain_gold(rule):
    tot += 1
    
print(tot)

def bags_in_bag(rule):
  tot = 0
  for num, bag in rules[rule]:
    tot += int(num) * (1 + bags_in_bag(bag))
  return tot

print(bags_in_bag('shiny gold'))