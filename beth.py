#!/usr/bin/env python3

from avionics.environmentals import SenseOfTime
from avionics.navigations import CoursePlotter
from utils.trough.Trough import Troughs, Trough

from src import args
from src.dns import collect
from src.domainscan import scan
from src.reverseip import reverse

from modules.peek.reverseWhois import whoisQuery as reverseWhois
from modules.peek.whois import whoisQuery
from modules.verify import email
from modules.query.urlscan import query

from src.globals import structures as st

sot             = SenseOfTime()

modules         = args.parse()
module          = modules[0]
jobs            = vars(modules[1])

sessionTroughs  = Troughs()

def the_most_important_function(jobs):
  for job in jobs:
    args        = jobs[job]

    if 'options' in vars(modules[1]):
      options   = modules[1].options
    else:
      options   = None

    if job == 'urlscan':
      target      = args[0]
      jobTrough   = Trough(f'{module}#{job}#{target}#')

    try:
      if job == 'urlscan':
        CoursePlotter(
          module,
          job,
          query,
          *args,
          sessionTroughs=sessionTroughs,
          trough=jobTrough,
          options=options
        )
        break

      for target in jobs[job]:
        jobTrough   = Trough(f'{module}#{job}#{target}#')

        if job == 'dns':
          CoursePlotter(
            module,
            job,
            collect,
            *args,
            sessionTroughs=sessionTroughs,
            trough=jobTrough,
            options=options
          )
          break

        elif job == 'email':
          CoursePlotter(
            module,
            job,
            email.verify,
            *args,
            sessionTroughs=sessionTroughs,
            trough=jobTrough,
            options=options
          )
          break

        elif job == 'reverse':
          CoursePlotter(
            module,
            job,
            reverse,
            *args,
            sessionTroughs=sessionTroughs,
            trough=jobTrough,
            options=options
          )
          break

        elif job == 'scan':
          CoursePlotter(
            module,
            job,
            scan,
            *args,
            sessionTroughs=sessionTroughs,
            trough=jobTrough,
            options=options
          )
          break

        elif job == 'whois':
          CoursePlotter(
            module,
            job,
            whoisQuery,
            *args,
            sessionTroughs=sessionTroughs,
            trough=jobTrough,
            options=options
          )
          break

        elif job == 'rwhois':
          CoursePlotter(
            module,
            job,
            reverseWhois,
            *args,
            sessionTroughs=sessionTroughs,
            trough=jobTrough,
            options=options
          )
          break

    except KeyboardInterrupt:
      break

    except Exception as f:
      raise(f)

the_most_important_function(jobs)
