# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 23:59:55 2020

@author: Mark Ferguson
"""
from copy import deepcopy

with open('inputs/input8.txt') as fh:
  lines = [line.strip() for line in fh.readlines()]

program = [line.split() for line in lines]

visited = []
accumulator = 0
line = 0
while line not in visited:
  instr = program[line][0]
  num = int(program[line][1])
  visited.append(line)
  
  if instr == 'nop':
    line += 1
  elif instr == 'jmp':
    line += num
  else:
    line += 1
    accumulator += num
   
print(accumulator)

def run(program):
  lines = len(program)
  visited = []
  accumulator = 0
  line = 0
  while True:
    if line == lines:
      return accumulator
    elif line > lines:
      return False
    if line in visited:
      return False
    
    instr = program[line][0]
    num = int(program[line][1])
    visited.append(line)
    
    if instr == 'nop':
      line += 1
    elif instr == 'jmp':
      line += num
    else:
      line += 1
      accumulator += num

  return False

swap = {'nop':'jmp', 'jmp':'nop'}
candidates = []
for line_no, line in enumerate(program):
  instr = line[0]
  if instr in ['nop', 'jmp']:
    candidates.append([line_no, swap[instr]])

for line, instr in candidates:
  prog = deepcopy(program)
  prog[line][0] = instr
  res = run(prog)
  if res:
    print(res)
    break
  