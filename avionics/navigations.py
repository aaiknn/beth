#!/usr/bin/env python3

from avionics.environmentals import SenseOfTime
from sessions.exceptions import NavigationException

from src.globals import structures as st

jobNames = {
  'dns'     : 'DNS',
  'email'   : 'Email Address',
  'reverse' : 'Reverse IP',
  'rwhois'  : 'Reverse Whois',
  'scan'    : 'Urlscan Site Scan',
  'shodan'  : 'Shodan',
  'status'  : 'HTTP Response Status',
  'up'      : 'HTTP Response Up',
  'urlscan' : 'Urlscan Search',
  'whois'   : 'Whois'
}

class CoursePlotter():
  def __init__(self, module, job, func, *args, **options):
    self.plot(module, job, func, *args, **options)

  def end_graciously(self, sessionTroughs, trough):
    sessionTroughs.entries.append(trough)
    print(st['glorious_separation'])
  
  def plot(self, module, job, func, *args, **options):
    _options    = options.get('options')
    sTs         = options.get('sessionTroughs')
    trough      = options.get('trough')

    target      = args[0]
    sot         = SenseOfTime()
    timestamp   = sot.get_time()

    print(st['glorious_separation'])
    print(
      'module  :', module,
      '\njob     :', jobNames[job],
      '\ntarget  :', target,
      '\ndate    :', timestamp
    )

    if _options is not None:
      print('options :', str(_options))

    print(st['glorious_separation'])

    try:
      trough = func(trough, *args, options=_options)

    except Exception as f:
      raise NavigationException(f)

    finally:
      self.end_graciously(sTs, trough)
