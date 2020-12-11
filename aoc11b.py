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

rows = len(plane)
cols = len(plane[0])

def seat_state(seat, plane):
  try:
    ret = plane[seat[0]][seat[1]] 
  except IndexError:
    print(seat)
    raise
  return ret

def is_valid(seat, rows=rows, cols=cols):
  if seat[0] < 0 or seat[0] == rows:
    return False
  if seat[1] < 0 or seat[1] == cols:
    return False
  return True

def somebody_there(seat, plane, direction, rows=rows, cols=cols):
  while True:
    seat = seat[0] + direction[0], seat[1] + direction[1]
    if is_valid(seat):
      state = seat_state(seat, plane)
      if state == '#':
        return True
      elif state == 'L':
        return False
    else:
      break
  return False


def check_filled(seat, plane):
  row, col = 0, 0
  l, r = -1, 1
  u, d = -1, 1
  up = u, col
  down = d, col
  left = row, l
  right = row, r
  u_l = u, l
  u_r = u, r
  d_l = d, l
  d_r = d, r
  people = 0
  for adj in (up, down, left, right, u_l, u_r, d_l, d_r):
    if somebody_there(seat, plane, adj):
      people += 1
  return people

def update(seat, plane):
# If a seat is empty (L) and there are no occupied 
# seats adjacent to it, the seat becomes occupied.
# If a seat is occupied (#) and four or more seats 
# adjacent to it are also occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.
  state = seat_state(seat, plane)
  can_see = check_filled(seat, plane)
  if state == 'L':
    if can_see == 0:
      return '#'
  elif state == '#':
    if can_see >= 5:
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
  disp(current_plane)

    
print(occupied(current_plane))