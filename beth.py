#!/usr/bin/env python3

from src import args
from src.dns import collect

jobs = args.parse()

glorious_separation = '------------------------------------------------'

def end_graciously():
    print(glorious_separation)

for module in jobs:
  for target in jobs[module]:
    print(glorious_separation)
    print('module:', module, 'target:', target)
    print(glorious_separation)

    if module == 'dns':
      records = collect(target)
      end_graciously()
      break

    elif module == 'reverse':
      end_graciously
      break
