# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 10:04:04 2020

@author: Mark Ferguson
"""

with open('inputs/input12.txt') as fh:
  plan = [line.strip() for line in fh.readlines()]
plan = [(step[0], int(step[1:])) for step in plan]

rotate = {
  'R':{
    90:lambda loc: (loc[1], -loc[0]), 
    180:lambda loc: (-loc[0], -loc[1]), 
    270:lambda loc: (-loc[1], loc[0])
  },
  'L':{
    90:lambda loc: (-loc[1], loc[0]), 
    180:lambda loc: (-loc[0], -loc[1]),
    270:lambda loc: (loc[1], -loc[0])
  }
}

move = {
  'N': lambda loc, distance: (loc[0], loc[1] + distance),
  'E': lambda loc, distance: (loc[0] + distance, loc[1]),
  'W': lambda loc, distance: (loc[0] - distance, loc[1]),
  'S': lambda loc, distance: (loc[0], loc[1] - distance)
}

def update_loc(loc, instruction, step):
  here, waypoint = loc
  if instruction in 'NEWS':
    waypoint = move[instruction](waypoint, step)
  elif instruction in 'RL':
    waypoint= rotate[instruction][step](waypoint)
  elif instruction == 'F':
    for _ in range(step):
      here = here[0] + waypoint[0], here[1] + waypoint[1]
  return here, waypoint

here = ((0, 0), (10, 1))
for instruction, step in plan:
  print(here, instruction, step)
  here = update_loc(here, instruction, step)
  print(f'--->{here}')
  print()
print(here)

print(abs(here[0][0])+abs(here[0][1]))
