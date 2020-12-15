# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 08:25:52 2020

@author: Mark Ferguson
"""
test_data = {
  436:[0,3,6],
  1:[1,3,2],
  10:[2,1,3],
  27:[1,2,3],
  78:[2,3,1],
  438:[3,2,1],
  1836:[3,1,2],
}
data = [8,13,1,0,18,9]

def play(start, n):
  # Start up
  play = len(start)
  last = dict(zip(start[:-1], range(1, play)))
  say = start[-1]
  while play <= n:
    if say in last:
      recent = last[say]
    else:
      recent = play
    said = say
    last[say] = play
    say = play - recent
    play += 1
  return said

for expected, start in test_data.items():
  print(expected, play(start, 2020))

print(play(data, 2020))

print(play(data,30000000))
