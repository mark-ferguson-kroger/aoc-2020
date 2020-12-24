# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 00:01:42 2020

@author: Mark Ferguson
"""
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from collections import defaultdict
import numpy as np
from re import compile
with open('inputs/test24.txt') as fh:
  lines = [line.strip() for line in fh.readlines()]

pattern = compile('(e|se|sw|w|nw|ne)')
paths = []
for line in lines:
  paths.append(pattern.findall(line))

class Floor:
  
  def __init__(self, layers=5):
    self.tiles = {(0,0,0):0}
    self.limits = ((0,0), (0,0), (0,0))
    self.active = {(0,0,0):0}
    self.go = {
          'w': lambda x,y,z: (x-1, y+1, z),
          'nw': lambda x,y,z: (x, y+1, z-1),
          'ne': lambda x,y,z: (x+1, y, z-1),
          'e': lambda x,y,z: (x+1, y-1, z),
          'se': lambda x,y,z: (x, y-1, z+1),
          'sw': lambda x,y,z: (x-1, y, z+1),
    }
    self.check = []
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
    self.set_limits()
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
      # self.show_path(path)
    self.active = self.count_em(self.tiles)

  def show_path(self, path, p=False):
    here = (0,0,0)
    cells = {here:0}
    visited = defaultdict(int)
    visited[here] += 1
    for step in path: 
      here = self.go[step](*here)
      if p: print(here)
      cells[here] = 0
      visited[here] += 1
    cells[here] = 1
    if p: print(visited)
    self.show_floor(floor=(cells,visited))
    
  
  def set_limits(self):
    xlim, ylim, zlim = self.limits
    for tile in self.tiles:
      x, y, z = tile
      xlim = min(x, xlim[0]), max(x, xlim[1])
      ylim = min(y, ylim[0]), max(y, ylim[1])
      zlim = min(y, ylim[0]), max(y, ylim[1])
    self.limits = (xlim, ylim, zlim)

  def count_one(self, tile):
      blacks = 0
      for nabe in self.neighbors(tile):
        if tile in self.check: print(tile, blacks, nabe)
        try: blacks += (self.tiles[nabe] % 2)
        except KeyError: pass
      return blacks
    
  def count_em(self, tiles):
    active = {}
    for tile in tiles:
      active[tile] = self.count_one(tile)
      if tile in self.check: print(tile, blacks)
    return active
  
  def new_state(self, tile):
    blacks = self.active[tile]
    if tile in self.check: 
      print(f'Updating {tile}, {blacks}')
      print(f'{tile} state = {self.tiles[tile]} active = {self.active[tile]}')
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

  def show_floor(self, scale=0.15, floor=None):
    colors = {1:"green", 0:"blue"}
    if not floor:
      tiles = self.tiles
      active = self.active
    else:
      tiles, active = floor
    m = scale * np.sin(np.radians(60))
    coord  = lambda x, y, z: (scale * (x - y) / 2, -m * z)
    
    fig, ax = plt.subplots(1)
    fig.set_dpi(250)
    ax.set_aspect('equal')
    ax.axis('off')
    
    def get_color(loc):
      if loc == (0,0,0): return 'red'
      return colors[tiles[loc] % 2]
    
    # Add some coloured hexagons
    xlim = -1, 1
    ylim = -1, 1
    for location, state in tiles.items():
      x, y = coord(*location)
      xlim = min(x, xlim[0]), max(x, xlim[1])
      ylim = min(y, ylim[0]), max(y, ylim[1])
      hex = RegularPolygon(
        (x, y),
        numVertices=6, 
        radius=scale/np.sqrt(3), 
        orientation=np.radians(60), 
        facecolor=get_color(location), 
        alpha=1, 
        edgecolor='k'
      )
      ax.add_patch(hex)
      ax.text(x, y + scale*0.2, str(active[location]),
              ha='center', va='center', size=4)
      ax.text(x, y - scale*0.1, str(location),
              ha='center', va='center', size=3)
    ax.set(xlim=xlim, ylim=ylim)
    return ax


     
floor = Floor()
floor.locate(paths)
floor.show_floor()
print(floor.count())
floor.update(1)
floor.show_floor()
print(floor.count())
