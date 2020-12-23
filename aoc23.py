# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 10:53:17 2020

@author: Mark Ferguson
"""
from time import time
test = '389125467'
data = '653427918'

class Circle:
  def __init__(self, cups, n=9):
    data = list(range(1,n+1))
    for i, c in enumerate(cups):
      data[i] = int(c)
    self.cups = data
    self.head = data[0]
    self.max = n
    self.next = {}
    self.loc = {}
    for i, c in enumerate(data):
      self.loc[c] = i
      try:
        self.next[c] = data[i+1]
      except IndexError:
        self.next[c] = data[0]

  def destination(self, pulled):
    target = self.head - 1
    if target == 0: target = self.max
    while target in pulled:
      target -= 1
      if target == 0: target = self.max
    return target

  def move(self):
    pulled = []
    here = self.head
    for i in range(3):
      pulled.append(self.next[here])
      here = self.next[here]
    dest = self.destination(pulled)
    self.next[self.head] = self.next[pulled[-1]]
    nxt = self.next[dest]
    self.next[dest] = pulled[0]
    self.next[pulled[-1]] = nxt
    self.head = self.next[self.head]
    
  def show(self):
    if self.max > 10:
      return None
    out = ''
    here = self.head
    while self.next[here] != self.head:
      out += str(here)
      here = self.next[here]
    return out + str(here)
  
  def output(self):
    if self.max > 10:
      return None
    out = ''
    here = self.next[1]
    while self.next[here] > 1:
      out += str(here)
      here = self.next[here]
    return out + str(here)
  
  def star(self):
    return self.next[1] * self.next[self.next[1]]
      
  
circle = Circle(data)
t = time()
for i in range(100):
  circle.move()
print(circle.output())

circle = Circle(data, n=1_000_000)

t = time()
for i in range(10_000_000):
  circle.move()
print(circle.star())
print(time() - t)