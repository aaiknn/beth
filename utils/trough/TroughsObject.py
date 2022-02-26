#!/usr/bin/env python3

from os import walk

class TroughsObject():
  def __init__(self, filename):
    self.identifier = filename
    self.data = ''

    for root, dirs, files in walk('trough'):
      if self.identifier in files:
        if self.identifier != '.keepme':
          with open(f'trough/{self.identifier}') as nom:
            data = nom.read()
            self.data += data
      else:
        print('Created new trough.')
