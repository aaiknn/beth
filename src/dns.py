#!/usr/bin/env python3

import dns.resolver

rTypes        = ['A', 'AAAA', 'CNAME','NS', 'MX', 'PTR', 'SOA', 'TXT']

class Records:
  def __init__(self):
    for rtype in rTypes:
      self.__setitem__(rtype, [])

  def __setitem__(self, key, value):
    setattr(self, key, value)
  
  def __getitem__(self, key):
    return getattr(self, key)
  
  def add_item(self, key, value):
    current = self.__getitem__(key)
    current.append(value)
    self.__setitem__(key, current)

def pull(records, target):
  for rtype in rTypes:
    try:
      response      = dns.resolver.query(target, rtype)
    except Exception as f:
      f_name = str(type(f).__name__)
      print(f_name, ':', f)
      continue

    for part in response:
      records.add_item(rtype, part)

def draw(records):
  for result in vars(records):
    if len(records[result]) > 0:
      print('')
      print(str(result))

      for entry in records[result]:
        print(str(entry))

def collect(trough, *args, **options):
  records       = Records()

  pull(records, args[0])
  draw(records)
