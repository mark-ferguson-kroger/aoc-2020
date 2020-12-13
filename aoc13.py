# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 23:46:08 2020


@author: Mark Ferguson
"""

with open('inputs/input13.txt') as fh:
  time = int(fh.readline().strip())
  bus_list = fh.readline().strip().split(',')

buses = [int(bus) for bus in bus_list if bus != 'x']

def time_diff(time, bus):
  q, r = divmod(time, bus)
  return (bus - r) % bus

diffs = {bus:time_diff(time, bus) for bus in buses}

min_diff = max(buses)
best_bus = -1
for bus, diff in diffs.items():
  if diff < min_diff:
    min_diff = diff
    best_bus = bus

print(best_bus * min_diff)

targets = {
  int(bus):(idx % int(bus)) 
  for idx, bus in enumerate(bus_list) if bus != 'x'
}

# Stolen brazenly from 
# https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
from functools import reduce
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
n_ = []
a_ = []
for n, a in targets.items():
  n_.append(n)
  a_.append(n-a)  

x = chinese_remainder(n_, a_) 
