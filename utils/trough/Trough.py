#!/usr/bin/env python3

class Troughs():
  def __init__(self):
    self.entries = []

  def persist(self):
    for entry in self.entries:
      with open(f'trough/{entry.identifier}', 'w') as file:
        file.write(str(entry.data))

class Trough():
  def __init__(self, identifier):
    self.identifier = identifier
    self.data = []
