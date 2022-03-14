#!/usr/bin/env python3

from avionics.environmentals import SenseOfTime
from avionics.navigations import CoursePlotter
from sessions.exceptions import SessionWarning
from utils.trough.Troughs import Troughs
from utils.trough.Trough import Trough

from src import args
from src.dns import collect
from src.domainscan import scan
from src.reverseip import reverse

from modules.peek.reverseWhois import whoisQuery as reverseWhois
from modules.peek.whois import whoisQuery
from modules.query.urlscan import query
from modules.stare.shodan import query as shodanQuery
from modules.test.httpresponse import is_it_up, whats_the_status
from modules.verify.email import verify

sot             = SenseOfTime()

modules         = args.parse()
module          = modules[0]
jobs            = vars(modules[1])

if 'options' in vars(modules[1]):
  options       = modules[1].options
  del jobs['options']
else:
  options       = None

try:
  sessionTroughs  = Troughs()
  sessionTroughs.retrieve_all()
except SessionWarning as w:
  print(w)
except Exception as f:
  raise f

def the_most_important_function(jobs):
  for job in jobs:
    args        = jobs[job]
    jobMap      = {
      'dns'     : collect,
      'email'   : verify,
      'reverse' : reverse,
      'rwhois'  : reverseWhois,
      'scan'    : scan,
      'shodan'  : shodanQuery,
      'status'  : whats_the_status,
      'up'      : is_it_up,
      'urlscan' : query,
      'whois'   : whoisQuery
    }

    try:
      for target in jobs[job]:
        jobTrough   = Trough(
          f'{module}#{job}#{target}#',
          sessionTrough=sessionTroughs
        )

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
