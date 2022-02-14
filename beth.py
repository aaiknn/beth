#!/usr/bin/env python3

from src import args
from src.dns import collect
from src.domainscan import scan
from src.reverseip import reverse

from src.globals import structures as st 

jobs = args.parse()

def end_graciously():
    print(st['glorious_separation'])

for module in jobs:
  try:
    for target in jobs[module]:
      print(st['glorious_separation'])
      print('module:', module, '\ntarget:', target)
      print(st['glorious_separation'])

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
