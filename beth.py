#!/usr/bin/env python3

from src import args
from src.dns import collect
from src.domainscan import scan
from src.reverseip import reverse

from modules.verify import email

from src.globals import structures as st 

modules   = args.parse()
module    = modules[0]
jobs      = vars(modules[1])

def end_graciously():
    print(st['glorious_separation'])

def the_most_important_function(jobs):
  for job in jobs:

    try:
      for target in jobs[job]:
        print(st['glorious_separation'])
        print(
          'module :', module,
          '\njob    :', job,
          '\ntarget :', target)
        print(st['glorious_separation'])

        if job == 'dns':
          records = collect(target)
          end_graciously()
          break

        elif job == 'email':
          email.verify(target)
          end_graciously()
          break

        elif job == 'reverse':
          reverse(target)
          end_graciously()
          break

        elif job == 'scan':
          scan(target)
          end_graciously()
          break

    except KeyboardInterrupt:
      end_graciously()
      break

the_most_important_function(jobs)
