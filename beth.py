#!/usr/bin/env python3

from avionics.environmentals import SenseOfTime
from utils.trough.Trough import Troughs, Trough

from src import args
from src.dns import collect
from src.domainscan import scan
from src.reverseip import reverse

from modules.peek.whois import whoisQuery
from modules.verify import email
from modules.query.urlscan import query

from src.globals import structures as st

sot             = SenseOfTime()

modules         = args.parse()
module          = modules[0]
jobs            = vars(modules[1])

sessionTroughs  = Troughs()

def end_graciously(jobTrough):
  sessionTroughs.entries.append(jobTrough)
  print(st['glorious_separation'])

def the_most_important_function(jobs):
  for job in jobs:

    if job == 'urlscan':
      args        = jobs[job]
      target      = args[0]
      jobTrough   = Trough(f'{module}#{job}#{target}#')

    try:
      if job == 'urlscan':
        timestamp = sot.get_time()

        print(st['glorious_separation'])
        print(
          'module  :', module,
          '\njob     :', job,
          '\ntarget  :', target,
          '\ndate    :', timestamp
        )

        if 'options' in vars(modules[1]):
          print('options :', str(modules[1].options))
          print(st['glorious_separation'])

          try:
            jobTrough = query(jobTrough, *args, options=modules[1].options)
          except Exception as f:
            print(f)

        else:
          print(st['glorious_separation'])

          try:
            jobTrough = query(jobTrough, *args)
          except Exception as f:
            print(f)

        end_graciously(jobTrough)
        break

      for target in jobs[job]:
        jobTrough   = Trough(f'{module}#{job}#{target}#')
        timestamp   = sot.get_time()

        print(st['glorious_separation'])
        print(
          'module  :', module,
          '\njob     :', job,
          '\ntarget  :', target,
          '\ndate    :', timestamp
        )
        print(st['glorious_separation'])

        if job == 'dns':
          collect(target)
          end_graciously(jobTrough)
          break

        elif job == 'email':
          email.verify(target)
          end_graciously(jobTrough)
          break

        elif job == 'reverse':
          reverse(target)
          end_graciously(jobTrough)
          break

        elif job == 'scan':
          scan(target)
          end_graciously(jobTrough)
          break

        elif job == 'whois':
          whoisQuery(target)
          end_graciously(jobTrough)
          break

    except KeyboardInterrupt:
      end_graciously(jobTrough)
      break

the_most_important_function(jobs)

if len(sessionTroughs.entries) > 0:
  sessionTroughs.persist()
