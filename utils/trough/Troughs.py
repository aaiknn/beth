#!/usr/bin/env python3

from os import walk
from json import dumps

from utils.trough.TroughsObject import TroughsObject

# *-- Troughs
#     |
#     *-- desc: entirety of TroughsObject class objects (aka: EVERYTHING!)
#     *-- creates and holds TroughsObject class objects
#              |
#              *-- desc: entirety of Trough class objects
#              *-- holds information on all persisted troughs
#              *-- holds Trough
#                       |
#                       *-- desc: entirety of TroughObject class objects for a given job
#                       *-- hold information on all persisted jobs
#                       *-- hold TroughObject
#                                |
#                                *-- desc: entirety of yielded data from a target
#                                *-- hold yielded information from specific targets

class Troughs():
  def __init__(self):
    self.identifier   = ''
    self.meta         = ''
    self.description  = ''
    self.entries      = []

  def persist_all(self):
    for trough in self.entries:
      entries         = []

      for t_object in trough.entries:
        t_items       = []

        for i_object in t_object['entries']:
          i_data      = {
            'identifier' : i_object['identifier'],
            'data'       : i_object['data'],
            'parent'     : i_object['parent']
          }
          t_items.append(i_data)

        t_data        = {
          'identifier'  : t_object['identifier'],
          'description' : t_object['description'],
          'entries'     : i_data
        }
        entries.append(t_data)

      data            = {
        'identifier'  : trough.identifier,
        'meta'        : trough.meta,
        'description' : trough.description,
        'entries'     : entries
      }

      with open(f'trough/{trough.identifier}', 'w') as file:
        file.write(dumps(data))

    return dumps(data)

  def retrieve_all(self):
    i = 0

    for root, dirs, files in walk('trough'):
      for name in files:
        if name == '.keepme':
          continue
        else:
          to = TroughsObject(name, parent=self)
          to = to.open()
          i = i+1

    print(f'LOG INFO: Retrieved {i} persisted troughs from storage.')
