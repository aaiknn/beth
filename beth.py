#!/usr/bin/env python3

from avionics.navigations import CoursePlotter
from sessions.exceptions import SessionWarning
from utils.trough.Troughs import Troughs
from src import args

modules         = args.parse()
module          = modules[0]
jobs            = vars(modules[1])

try:
  sessionTroughs  = Troughs()
  sessionTroughs.retrieve_all()
except SessionWarning as w:
  print(w)
except Exception as f:
  raise f

def whats_up_doc(jobs):
  options         = {}

  if 'mode' in jobs:
    options.update({
      'mode' : modules[1].mode
    })
    del jobs['mode']

  if 'options' in jobs:
    options.update({
      'constants' : [modules[1].options]
    })
    del jobs['options']

  if 'verbosity' in jobs:
    options.update({
      'verbosity' : modules[1].verbosity
    })
    del jobs['verbosity']

  prepositions = [
    'after',
    'before',
    'between'
  ]

  for item in prepositions:
    if item in jobs:
      _dict = {
        'prepositions' : { item : jobs[item] }
      }
      options.update(_dict)
      del jobs[item]

  return options

def the_most_important_function(jobs, options):
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

options = whats_up_doc(jobs)
the_most_important_function(jobs, options)
