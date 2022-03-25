#!/usr/bin/env python3

from avionics.environmentals import SenseOfTime
from avionics.navigations import CoursePlotter
from sessions.exceptions import SessionWarning
from utils.trough.Troughs import Troughs

from src import args

sot             = SenseOfTime()

modules         = args.parse()
module          = modules[0]
jobs            = vars(modules[1])

if 'options' in vars(modules[1]):
  options       = [modules[1].options]
  del jobs['options']
else:
  options       = []

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

    try:
      for target in jobs[job]:
        CoursePlotter(
          module,
          job,
          target,
          *args,
          sessionTroughs=sessionTroughs,
          options=options
        )
        break

    except KeyboardInterrupt:
      break

    except Exception as f:
      raise(f)

the_most_important_function(jobs)
