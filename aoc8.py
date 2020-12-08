# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 23:59:55 2020

@author: Mark Ferguson
"""
from re import compile

with open('inputs/input8.txt') as fh:
  lines = [line.strip() for line in fh.readlines()]


commands = ('acc', 'jmp', 'nop')

com_str = '|'.join(commands)

instructions = compile(f"({com_str})\s+([+-]\d+)")

program = [list(instructions.match(line).groups()) for line in lines]

program = list(zip(range(len(program)), program))

visited = []
accumulator = 0
line = 0
while program[line][0] not in visited:
  instr = program[line][1][0]
  num = int(program[line][1][1])
  visited.append(program[line][0])
  
  if instr == 'nop':
    line += 1
  elif instr == 'jmp':
    line += num
  else:
    line += 1
    accumulator += num
   
print(accumulator)

def run(program, swap_line):
  visited = []
  accumulator = 0
  line = 0
  while True:
    if line == len(program):
      return accumulator
    try:
      line_no = program[line][0]
    except IndexError:
      return False
    if line_no in visited:
      return False
    instr = program[line_no][1][0]
    num = int(program[line_no][1][1])
    visited.append(line_no)
    
    if line == swap_line:
      if instr == 'nop':
        do = 'jmp'
      elif instr == 'jmp':
        do = 'nop'
      else:
        do = 'acc'
    else:
      do = instr
    if do == 'nop':
      line += 1
    elif do == 'jmp':
      line += num
    else:
      line += 1
      accumulator += num
  return False

candidates = []
for line in program:
  instr = line[1][0]
  if instr in ['nop', 'jmp']:
    candidates.append(line[0])

for switch in candidates:
  res = run(program, switch)
  if res:
    print(res)
    break
  
