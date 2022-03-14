#!/usr/bin/env python3

from os import walk
from json import loads

from sessions.exceptions import SessionWarning
from utils.trough.Trough import Trough
from utils.trough.TroughObject import TroughObject

class TroughsObject():
  def __init__(self, identifier, parent):
    self.identifier   = identifier
    self.meta         = ''
    self.description  = ''
    self.entries      = []

  def open(self):
    for root, dirs, files in walk('trough'):
      if self.identifier in files:

        with open(f'trough/{self.identifier}') as nom:
          data = nom.read()
          _dict = loads(data)

          self.meta         = _dict['meta']
          self.description  = _dict['description']

          for entry in _dict['entries']:
            t_entries       = []

            for item in entry['entries']:
              to            = TroughObject(
                item['identifier'],
                meta        = item['meta'],
                description = item['description'],
                data        = item['data'],
                parent      = item['parent']
              )
              t_entries.append(to)

            trough          = Trough(
              entry['identifier'],
              entry['meta'],
              entry['description'],
              t_entries
            )
            self.entries.append(trough)

      else:
        raise SessionWarning(f'LOG INFO: Trough {self.identifier} hasn\'t yet been persisted.')

      return self
