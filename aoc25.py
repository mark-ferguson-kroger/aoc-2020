# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 23:53:53 2020

@author: Mark Ferguson
"""
data = [12090988, 240583]

def transform(n, subject=7):
  return pow(subject, n, 20201227)

def secret(pubkey, subject=7):
  i = 0
  val = None
  while val != pubkey: i, val = i+1, transform(i, subject=7)
  return i-1

def handshake(key1, key2):
  sec2 = secret(key2)
  return transform(sec2, subject=key1)

print(handshake(*data))