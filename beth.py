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

sot             = SenseOfTime()

modules         = args.parse()
module          = modules[0]
jobs            = vars(modules[1])

sessionTroughs  = Troughs()

def the_most_important_function(jobs):
  for job in jobs:
    args        = jobs[job]
    jobMap      = {
      'dns'     : collect,
      'email'   : email.verify,
      'reverse' : reverse,
      'rwhois'  : reverseWhois,
      'scan'    : scan,
      'urlscan' : query,
      'whois'   : whoisQuery
    }

    if 'options' in vars(modules[1]):
      options   = modules[1].options
    else:
      options   = None

    try:
      for target in jobs[job]:
        jobTrough   = Trough(f'{module}#{job}#{target}#')

        CoursePlotter(
          module,
          job,
          jobMap[job],
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
