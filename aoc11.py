# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 23:56:53 2020

@author: Mark Ferguson
"""
from copy import deepcopy

def chars(line):
  return [char for char in line]

with open('inputs/input11.txt') as fh:
  plane = [chars(line.strip()) for line in fh.readlines()]

def seat_state(seat, plane):
  try:
    ret = plane[seat[0]][seat[1]] 
  except IndexError:
    print(seat)
    raise
  return ret

def flip_empty(seat, plane):
  rows = len(plane)
  cols = len(plane[0])
  row, col = seat[0], seat[1]
  l, r = col - 1, col + 1
  u, d = row - 1, row + 1
  up = u, col
  down = d, col
  left = row, l
  right = row, r
  u_l = u, l
  u_r = u, r
  d_l = d, l
  d_r = d, r
  if u < 0: 
    up, u_l, u_r = None, None, None
  if d == rows: 
    down, d_l, d_r = None, None, None
  if l < 0: 
    left, u_l, d_l = None, None, None
  if r == cols:
    right, d_r, u_r = None, None, None
  all_empty = True
  for adj in (up, down, left, right, u_l, u_r, d_l, d_r):
    if adj and seat_state(adj, plane) == '#':
      all_empty = False
      break
  return all_empty

def flip_filled(seat, plane):
  rows = len(plane)
  cols = len(plane[0])
  row, col = seat[0], seat[1]
  l, r = col - 1, col + 1
  u, d = row - 1, row + 1
  up = u, col
  down = d, col
  left = row, l
  right = row, r
  u_l = u, l
  u_r = u, r
  d_l = d, l
  d_r = d, r
  if u < 0: 
    up, u_l, u_r = None, None, None
  if d == rows: 
    down, d_l, d_r = None, None, None
  if l < 0: 
    left, u_l, d_l = None, None, None
  if r == cols:
    right, d_r, u_r = None, None, None
  occupied = 0
  for adj in (up, down, left, right, u_l, u_r, d_l, d_r):
    if adj and seat_state(adj, plane) == '#':
      occupied += 1
  return occupied

def update(seat, plane):
# If a seat is empty (L) and there are no occupied 
# seats adjacent to it, the seat becomes occupied.
# If a seat is occupied (#) and four or more seats 
# adjacent to it are also occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.
  state = seat_state(seat, plane)
  if state == 'L':
    if flip_empty(seat, plane):
      return '#'
  elif state == '#':
    if flip_filled(seat, plane) >= 4:
      return 'L'
  return state

def plane_eq(plane1, plane2):
  for r in range(len(plane1)):
    for c in range(len(plane1[0])):
      if plane1[r][c] != plane2[r][c]:
        return False
  return True

def disp(plane):
  for row in plane:
    print(''.join(row))
  print()

  
rows = len(plane)
cols = len(plane[0])

def occupied(plane, rows=rows, cols=cols):
  tot = 0
  for row in range(rows):
    for col in range(cols):
      if plane[row][col] == '#':
        tot += 1
  return tot

current_plane = deepcopy(plane)
next_plane = deepcopy(plane)
while True:
  for row in range(rows):
    for col in range(cols):
      next_plane[row][col] = update((row,col), current_plane)
  if plane_eq(next_plane, current_plane):
    break
  current_plane = deepcopy(next_plane)
print(occupied(current_plane))