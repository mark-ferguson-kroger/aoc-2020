# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 00:01:42 2020

@author: Mark Ferguson
"""

from re import compile
with open('inputs/input24.txt') as fh:
  lines = [line.strip() for line in fh.readlines()]

pattern = compile('(e|se|sw|w|nw|ne)')
paths = []
for line in lines:
  paths.append(pattern.findall(line))

class Floor:
  
  def __init__(self, layers=30):
    self.tiles = {(0,0,0):0}
    self.active = {(0,0,0):0}
    self.go = {
          'w': lambda x,y,z: (x-1, y+1, z),
          'nw': lambda x,y,z: (x, y+1, z-1),
          'ne': lambda x,y,z: (x+1, y, z-1),
          'e': lambda x,y,z: (x+1, y-1, z),
          'se': lambda x,y,z: (x, y-1, z+1),
          'sw': lambda x,y,z: (x-1, y, z+1),
    }
    self.initialize(layers)

  def pad(self, update=False):
    extra = []
    for tile in self.tiles:
      for compass in self.go:
        address = self.go[compass](*tile)
        if address not in self.tiles:
          if update:
            if self.count_one(tile):
              extra.append(address)
          else:
            extra.append(address)
    return extra

  def initialize(self, layers):
    for _ in range(layers):
      new_layer = self.pad()
      for tile in new_layer:
        self.tiles[tile] = 0
        self.active[tile] = 0
    self.active = self.count_em(self.tiles)

  def neighbors(self, tile):
    nabes = []
    for compass in self.go:
      nabes.append(self.go[compass](*tile))
    return nabes
  
  def locate(self, paths):
    for path in paths:
      here = (0,0,0)
      for step in path: here = self.go[step](*here)
      self.tiles[here] += 1
    self.active = self.count_em(self.tiles)

  def count_one(self, tile):
      blacks = 0
      for nabe in self.neighbors(tile):
        try: blacks += (self.tiles[nabe] % 2)
        except KeyError: pass
      return blacks
    
  def count_em(self, tiles):
    active = {}
    for tile in tiles:
      active[tile] = self.count_one(tile)
    return active

  def new_state(self, tile):
    blacks = self.active[tile]
    if self.tiles[tile] % 2:
      if blacks == 0 or blacks > 2: return 0
      else: return 1
    else:
      if blacks == 2: return 1
      else: return 0

  def update(self, n):
    for i in range(n):
      extras = self.pad(update=True)
      for tile in extras:
        self.tiles[tile] = 0
        self.active[tile] = 0
      new_tiles = self.tiles.copy()
      for tile in self.tiles.keys(): new_tiles[tile] = self.new_state(tile)
      self.tiles = new_tiles
      self.active = self.count_em(new_tiles)
      print(f'Day {i+1}: {self.count()}')

  def count(self):
    blacks = 0
    for state in self.tiles.values():
      blacks += (state % 2)
    return blacks


     
floor = Floor()
floor.locate(paths)
print(floor.count())
floor.update(100)
print(floor.count())
