#!/usr/bin/env python3

from os import path
from fileinput import input
import dns.resolver

rTypes        = ['A', 'AAAA', 'CNAME','NS', 'MX', 'PTR', 'SOA', 'TXT']

def pull(target):
  for rtype in rTypes:
    output = ''
    try:
      response      = dns.resolver.query(target, rtype)

    except Exception as f:
      f_name = str(type(f).__name__)
      print(f_name, ':', f, '\n')
      continue

    else:
      output += f'{rtype}:\n'
      for line in response:
        output += f'  * {line}\n'
      output += '\n'
      print(output)

def prepData(_input, **options):
  _data             = []
  _options          = options.get('options')

  if 'constants' in _options.keys() and 'BULK_FILE' in _options['constants']:
    if path.exists(_input):
      with input(files=(_input)) as doc:
        for entry in doc:
          entry     = entry.split('\n')
          entry     = entry[0]
          _data.append(entry)

    else:
      raise FileNotFoundError(f'\'{_input}\' doesn\'t appear to be an existing path on your system.')

  else:
    _data.append(_input)

  return _data

def collect(trough, *args, **options):
  input        = args[0]

  try:
    _data       = prepData(input, **options)
  except Exception as f:
    raise f
  else:
    for loc in _data:
      if len(loc) > 0:
        if len(_data) > 1:
          print(f'Records for: {loc}')

        pull(loc)

        if len(_data) > 1:
          print('\n')

  return trough
