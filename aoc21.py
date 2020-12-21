# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 00:04:07 2020

@author: Mark Ferguson
"""
from collections import defaultdict, Counter
from functools import reduce
with open('inputs/input21.txt') as fh:
  data = [
    line.replace('(','').replace(')', '').strip()
    for line in fh.readlines()
  ]

might_have = defaultdict(list)
full_ingredients = []
def grok(info, might_have):
  ingredients, allergens = info.split(' contains ')
  ingredients = set(ingredients.split(' '))
  allergens = allergens.split(', ')
  for allergen in allergens:
    might_have[allergen].append(ingredients)
  return list(ingredients), might_have

for line in data:
  ingredients, might_have = grok(line, might_have)
  full_ingredients.extend(ingredients)

all_ingredients = set(full_ingredients)
must_have = defaultdict(set)
for allergen in might_have:
  must_have[allergen] = reduce(set.intersection, might_have[allergen])

clear = []
for ingredient in all_ingredients:
  if reduce(
      lambda x, y: x and y, 
      [ingredient not in allergens for allergens in must_have.values()]
  ):
    clear.append(ingredient)

tot = 0
counts = Counter(full_ingredients)
for ingredient in clear:
  tot += counts[ingredient]
  
print(tot)

def reduce_lists(must_have):
  danger = {}
  for allergen, ingredients in must_have.items():
    if len(ingredients) == 1:
      danger[allergen] = ingredients.pop()
  for allergen in danger:
    del must_have[allergen]
    for all_ in must_have.keys():
      must_have[all_].discard(danger[allergen])
  return danger, must_have

danger = {}
while must_have:
  danger_d, must_have = reduce_lists(must_have)
  danger.update(danger_d)

out = [danger[allergen] for allergen in sorted(danger.keys())]
print(','.join(out))