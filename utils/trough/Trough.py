#!/usr/bin/env python3

class Trough():
  def __init__(self, identifier, *args, **options):
    self.identifier   = identifier
    self.meta         = ''
    self.description  = ''
    self.entries      = []
    self.parent       = options.get('sessionTrough')

    if len(args) > 0:
      self.meta         = args[0]
      self.description  = args[1]
      self.entries      = args[2]

  def record_results(self):
    self.parent.entries.append(self)
