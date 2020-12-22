# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 00:04:41 2020

@author: Mark Ferguson
"""
import numpy as np
import re
from functools import reduce

def to_num(line):
  return [
    int(char) for char 
    in line.replace("#", "1").replace(".", "0").replace(" ", "0")
  ]

tiles = {}
with open('inputs/input20.txt') as fh:
  data = [line.strip() for line in fh.readlines()]
data.append('')
for line in data:
  match = re.match('Tile (\d+):', line)
  if match:
    tile_no = int(match.groups()[0])
    tiles[tile_no] = []
    continue
  if line:
    tiles[tile_no].append(to_num(line))
  else:
    tiles[tile_no] = np.array(tiles[tile_no])

n = int(np.sqrt(len(tiles)))
tile_nos = list(tiles.keys())
shape = tiles[tile_nos[0]].shape
last = shape[0] - 1
idx = list(range(shape[0]))

TOP, RIGHT, BOTTOM, LEFT = (0,idx), (idx,last), (last,idx), (idx,0)

def edges(tile):
  return tile[TOP], tile[RIGHT], tile[BOTTOM], tile[LEFT]

orient = {
  0: lambda tile: tile,
  1: lambda tile: np.rot90(tile),
  2: lambda tile: np.rot90(np.rot90(tile)),
  3: lambda tile: np.rot90(np.rot90(np.rot90(tile))),
  4: lambda tile: np.fliplr(tile),
  5: lambda tile: np.rot90(np.fliplr(tile)),
  6: lambda tile: np.rot90(np.rot90(np.fliplr(tile))),
  7: lambda tile: np.rot90(np.rot90(np.rot90(np.fliplr(tile))))
}

def lr_match(left, l_or, right, r_or):
  return all(edges(orient[l_or](left))[1] == edges(orient[r_or](right))[3])

def ud_match(top, t_or, bottom, b_or):
  return all(edges(orient[t_or](top))[2] == edges(orient[b_or](bottom))[0])

def list_matches(tile1, tile_nos=tile_nos):
  this_match = {}
  for tile2 in tile_nos:
    if tile1 == tile2: continue
    tile_1, tile_2 = tiles[tile1], tiles[tile2]
    for orientation in range(8):
      if lr_match(tile_1, 0, tile_2, orientation):
        this_match.update({tile2:(orientation,'right')})
        break
      if lr_match(tile_2, orientation, tile_1, 0):
        this_match.update({tile2:(orientation,'left')})
        break
      if ud_match(tile_1, 0, tile_2, orientation):
        this_match.update({tile2:(orientation,'below')})
        break
      if ud_match(tile_2, orientation, tile_1, 0):
        this_match.update({tile2:(orientation,'above')})
        break
  return this_match
      
matches = {tile:list_matches(tile) for tile in tile_nos}

tot = 1
edge_nos = {2:[], 3:[], 4:[]}
for tile in matches.keys():
  matched = len(matches[tile])
  edge_nos[matched].append({tile:matches[tile]})
  if matched == 2:
    tot *= tile
    
print(tot)

def stitch_lr(left, right):
  return np.append(left, right, axis=1)

def stitch_ud(top, bottom):
  return np.append(top, bottom, axis=0)

def get_adjacent(tile_no):
  adjacent = []
  for tile_num, (or_, pos) in matches[tile_no].items():
    adjacent.append(tile_num)
  return adjacent

def reorient_tile(tile_no, or_):
  tiles[tile_no] = orient[or_](tiles[tile_no])
  matches[tile_no] = list_matches(tile_no, get_adjacent(tile_no))
  return tiles[tile_no]

def get_right(tile_no):
  for tile_num, (or_, pos) in matches[tile_no].items():
    if pos == 'right':
      return tile_num, or_

def get_under(tile_no):
  for tile_num, (or_, pos) in matches[tile_no].items():
    if pos == 'below':
      tiles[tile_num] = reorient_tile(tile_num, or_)
      return tile_num

corner_pieces = []
for corner in edge_nos[2]:
  corner_pieces.append(list(corner.keys())[0])
edge_pieces = []
for edge in edge_nos[3]:
  edge_pieces.append(list(edge.keys())[0])

def build_row(tile_no):
  beneath = get_under(tile_no)
  if tile_no in corner_pieces:
    corner_pieces.remove(tile_no)
    end_pieces = corner_pieces
  else:
    edge_pieces.remove(tile_no)
    end_pieces = edge_pieces
  row = [tiles[tile_no]]
  last_tile = tile_no
  while last_tile not in end_pieces:
    next_tile, or_ = get_right(last_tile)
    if or_:
      row.append(reorient_tile(next_tile, or_))
    else:
      row.append(tiles[next_tile])
    last_tile = next_tile
  return row, beneath

# Start with an upper left piece
for edge_info in edge_nos[2]:
  tile_no = list(edge_info.keys())[0]
  adj = edge_info[tile_no]
  start = None
  has_below, has_right = False, False
  for neighbor, (or_, pos) in adj.items():
    if pos == 'below':
      has_below = True
    elif pos == 'right':
      has_right = True
    if has_below and has_right:
      start = tile_no
  if start:
    break

row, beneath = build_row(start)
picture = [row]
while beneath:
  row, beneath = build_row(beneath)
  picture.append(row)

def strip_border(tile):
  r, c = tile.shape
  return tile.copy()[1:(r-1), 1:(c-1)]

new_pic = []
for row in picture:
  this_row = []
  for tile in row:
    this_row.append(strip_border(tile))
  new_pic.append(reduce(lambda left, right: stitch_lr(left, right), this_row))
full_pic = reduce(lambda above, below: stitch_ud(above, below), new_pic)  

with open('inputs/input20-seamonster.txt') as fh:
  seamonster = np.array([to_num(line.replace('\n','')) for line in fh.readlines()])
with open('inputs/test20a.txt') as fh:
  ocean = np.array([to_num(line.replace('\n','')) for line in fh.readlines()])
  
height, length = seamonster.shape
def got_one(address, area):
  r, c = address
  down, right = r + height, c + length  
  scan = area[r:down, c:right]
  check = np.logical_and(seamonster, scan)
  return np.array_equal(seamonster, check)

tot = 0
for or_ in range(8):
  trial = orient[or_](full_pic.copy())
  for address in np.ndindex(trial.shape[0]-height, trial.shape[1] - length):
    if got_one(address, trial):
      tot += 1

print(np.sum(trial) - tot*np.sum(seamonster))