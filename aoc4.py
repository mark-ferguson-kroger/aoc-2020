# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 00:06:29 2020

@author: Mark Ferguson
"""

from re import compile

with open('inputs/input4.txt') as fh:
  lines = [line.strip() for line in fh.readlines()]

key_value = compile(r'(\w+):(#?\w+)')

def get_fields(this_id):
  pairs = key_value.findall(this_id)
  return {k:v for k,v in pairs}

def parse_ids(lines):
  ids = []
  this_id = ''
  for line in lines:
    if line == '':
      ids.append(get_fields(this_id))
      this_id = ''
    else:
      this_id = ' '.join([this_id, line])
  if this_id != '':
    ids.append(get_fields(this_id))
  return ids
        
ids = parse_ids(lines)    

def check_id(id_):
  keys = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
    # 'cid',
  ]
  for key in keys:
    if key not in id_.keys():
      return False
  return True

good = 0
for id_ in ids:
  if check_id(id_):
    good += 1
  
print(good)

yr = compile(r'^\d{4}$')
hgt_cm = compile(r'^(\d{3})cm$')
hgt_in = compile(r'^(\d{2})in$')
hcl = compile(r'^#[0-9a-f]{6}$')
pid = compile(r'^\d{9}$')
def year_check(val, least, most):
  if yr.match(val):
    num = int(val)
    if least <= num <= most:
      return True
  return False

def check_vals(id_):
  '''byr (Birth Year) - four digits; at least 1920 and at most 2002.'''
  if not year_check(id_['byr'], 1920, 2002):
    return False

  '''iyr (Issue Year) - four digits; at least 2010 and at most 2020.'''
  if not year_check(id_['iyr'], 2010, 2020):
    return False

  '''eyr (Expiration Year) - four digits; at least 2020 and at most 2030.'''
  if not year_check(id_['eyr'], 2020, 2030):
    return False

  '''hgt (Height) - a number followed by either cm or in:'''
  '''  If cm, the number must be at least 150 and at most 193.'''
  '''  If in, the number must be at least 59 and at most 76.'''
  h_cm = hgt_cm.match(id_['hgt'])
  h_in = hgt_in.match(id_['hgt'])
  if not (h_cm or h_in):
    return False
  if h_cm:
    h = int(h_cm.groups()[0])
    if not (150 <= h <= 193):
      return False
  else:
    h = int(h_in.groups()[0])
    if not (59 <= h <= 76):
      return False
  
  '''hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.'''
  if not hcl.match(id_['hcl']):
    return False
  
  '''ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.'''
  if id_['ecl'] not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
    return False
  
  '''pid (Passport ID) - a nine-digit number, including leading zeroes.'''
  if not pid.match(id_['pid']):
    return False
  
  '''cid (Country ID) - ignored, missing or not.'''
  return True

good = 0
for id_ in ids:
  if check_id(id_):
    if check_vals(id_):
      good += 1


print(good)