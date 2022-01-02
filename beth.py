#!/usr/bin/env python3

from src import args
from src.dns import collect
from src.domainscan import scan
from src.reverseip import reverse

jobs = args.parse()

glorious_separation = '------------------------------------------------'

def end_graciously():
    print(glorious_separation)

for module in jobs:
  try:
    for target in jobs[module]:
      print(glorious_separation)
      print('module:', module, '\ntarget:', target)
      print(glorious_separation)

      if module == 'dns':
        records = collect(target)
        end_graciously()
        break

      elif module == 'reverse':
        reverse(target)
        end_graciously()
        break

      elif module == 'scan':
        scan(target)
        end_graciously()
        break

  except KeyboardInterrupt:
    break
