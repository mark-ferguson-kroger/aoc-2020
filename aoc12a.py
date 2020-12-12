# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 10:04:04 2020

@author: Mark Ferguson
"""

with open('inputs/input12.txt') as fh:
  plan = [line.strip() for line in fh.readlines()]

plan = [(step[0], int(step[1:])) for step in plan]

r90 = {'N':'E', 'E':'S', 'S':'W', 'W':'N'}
r180 = {'N':'S', 'E':'W', 'S':'N', 'W':'E'}
r270 = {'N':'W', 'E':'N', 'S':'E', 'W':'S'}
turn = {
  'R':{90:r90, 180:r180, 270:r270},
  'L':{90:r270, 180:r180, 270:r90}
}

move = {
  'N': lambda loc, distance: (loc[0] + distance, loc[1]),
  'E': lambda loc, distance: (loc[0], loc[1] + distance),
  'W': lambda loc, distance: (loc[0], loc[1] - distance),
  'S': lambda loc, distance: (loc[0] - distance, loc[1])
}

def update_loc(loc, direction, step):
  facing = loc[0]
  here = loc[1]
  if direction in 'RL':
    facing = turn[direction][step][facing]
    return facing, here
  if direction == 'F':
    direction = facing
  here = move[direction](here, step)
  return facing, here
  

here = ('E', (0, 0))
for direction, step in plan:
  print(here, direction, step)
  here = update_loc(here, direction, step)
  print(f'--->{here}')
  print()
print(here)
