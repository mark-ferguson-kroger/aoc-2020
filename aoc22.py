# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 00:00:50 2020

@author: Mark Ferguson
"""
p1_ = []
p2_ = []
with open('inputs/input22.txt') as fh:
  p1_next, p2_next = False, False
  for line in fh.readlines():
    if line == '\n': continue
    if line == 'Player 1:\n':
      p1_next = True
      continue
    if line == 'Player 2:\n':
      p1_next, p2_next = False, True
      continue
    if p1_next: p1_.append(int(line.strip()))
    if p2_next: p2_.append(int(line.strip()))
      
def play(p1, p2):
  c1, c2 = p1.pop(0), p2.pop(0)
  if c1 > c2: p1.extend([c1, c2])
  else: p2.extend([c2, c1])
  return p1, p2

p1, p2 = p1_.copy(), p2_.copy()

while p1 and p2:
  p1, p2 = play(p1, p2)
 
def score(p):
  tot = 0
  for i, val in enumerate(reversed(p)): tot += (i+1)*val
  return tot

print(score(p1 + p2))

p1, p2 = p1_.copy(), p2_.copy()

decks = {1:p1, 2:p2}

def game(decks):
  history = []
  while decks[1] and decks[2]:
    state = (tuple(decks[1]), tuple(decks[2]))
    if state in history: return 1, decks
    history.append(state)
    c1, c2 = decks[1].pop(0), decks[2].pop(0)
    if c1 <= len(decks[1]) and c2 <= len(decks[2]):
      _p1, _p2 = decks[1][:c1].copy(), decks[2][:c2].copy()
      winner, _ = game({1:_p1, 2:_p2})
    else:
      if c1 > c2: winner = 1
      else: winner = 2
    if winner == 1: decks[1].extend([c1, c2])
    else: decks[2].extend([c2, c1])
  if decks[1]: winner = 1
  else: winner = 2
  return winner, decks

winner, decks = game(decks)
print(score(decks[1] + decks[2]))