# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 21:14:46 2020

@author: Mark Ferguson
"""
from re import compile
from collections import defaultdict
mask_re = compile(r'^mask = ([X10]*)')
value_re = compile(r'^mem\[(\d+)\] = (\d+)+')
with open('inputs/input14.txt') as fh:
  data = [line.strip() for line in fh.readlines()]
  
masks = []
instructions = []
acc = None
for line in data:
  mask = mask_re.findall(line)
  if mask:
    masks.append(mask[0])
    if acc is not None:
      instructions.append(acc)
    acc = []
  else:
    acc.append(value_re.findall(line)[0])
instructions.append(acc)

def parse_mask(mask):
  values = [
    (idx, val) for idx, val in
      enumerate(mask)
      if val != 'X'
  ]
  return values

def apply_mask(number, mask):
  values = parse_mask(mask)
  bi = format(int(number), '036b')
  for idx, val in values:
    bi = bi[:idx] + f'{val}' + bi[(idx+1):]
  return int(bi, 2)

memory = defaultdict(int)
for mask, instruction in zip(masks, instructions):
  for loc, val in instruction:
    memory[loc] = apply_mask(val, mask)
    
print(sum(list(memory.values())))

# Part 2

def parse_mask2(mask):
  values = [
    (idx, val) for idx, val in
      enumerate(mask)
      if val != '0'
  ]
  return values


def mask_addresses(address, mask):
  values = parse_mask2(mask)
  bi = format(int(address), '036b')
  addresses = []
  digits = []
  for idx, val in values:
    if val == '1':
      bi = bi[:idx] + '1' + bi[(idx+1):]
    else:
      digits.append(idx)
  n = len(digits)
  floats = [format(i, f'0{n}b') for i in range(2**(n))]
  for flt in floats:
    b = bi
    for slot, bit in zip(digits, flt):
      b = b[:slot] + bit + b[(slot+1):]
    addresses.append(int(b,2))
  return addresses
  
memory = defaultdict(int)
for mask, instruction in zip(masks, instructions):
  for loc, val in instruction:
    addresses = mask_addresses(loc, mask)
    for address in addresses:
      memory[address] = int(val)

print(sum(list(memory.values())))
