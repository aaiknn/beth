#!/usr/bin/env python3

class TroughObject():
  def __init__(self, identifier, *args, **options):
    self.identifier       = identifier
    self.meta             = options.get('meta')
    self.desciption       = options.get('description')
    self.data             = options.get('data')
    self.parent           = options.get('parent')

    self.parent.entries.append(self)
