#!/usr/bin/env python3

from avionics.environmentals import SenseOfTime
from sessions.exceptions import NavigationException
from utils.trough.Trough import Trough

from src.dns import collect
from src.domainscan import scan
from src.reverseip import reverse

from modules.peek.reverseWhois import whoisQuery as reverseWhois
from modules.peek.whois import whoisQuery
from modules.query.urlscan import query
from modules.stare.shodan import query as shodanQuery
from modules.test.httpresponse import is_it_up, whats_the_status
from modules.verify.email import verify

from src.globals import structures as st

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

jobTitles = {
  'dns'     : 'DNS',
  'email'   : 'Email Address',
  'reverse' : 'Reverse IP',
  'rwhois'  : 'Reverse Whois',
  'scan'    : 'Urlscan Site Scan',
  'shodan'  : 'Shodan',
  'status'  : 'HTTP Response Status',
  'up'      : 'HTTP Response',
  'urlscan' : 'Urlscan Search',
  'whois'   : 'Whois'
}

class CoursePlotter():
  def __init__(self, module, job, target, *args, **options):
    self.plot(module, job, target, *args, **options)

  def create_trough(self, module, job, target, sessionTrough):
    trough   = Trough(
      f'{module}#{job}#{target}#',
      sessionTrough=sessionTrough
    )
    return trough

  def end_graciously(self, sessionTroughs, trough):
    sessionTroughs.entries.append(trough)
    print(st['glorious_separation'])
  
  def plot(self, module, job, target, *args, **options):
    _options    = options.get('options')
    sTs         = options.get('sessionTroughs')
    sot         = SenseOfTime()
    timestamp   = sot.get_time()
    func        = jobMap[job]

    trough      = self.create_trough(module, job, target, sTs)

    print(st['glorious_separation'])
    print(
      'Module  :', module,
      '\nJob     :', jobTitles[job],
      '\nTarget  :', target,
      '\nDate    :', timestamp
    )

    if 'constants' in _options.keys() and len(_options['constants']) > 0:
      print('Options :', str(_options['constants']))

    print(st['glorious_separation'])

    try:
      trough = func(trough, *args, options=_options)

    except Exception as f:
      raise NavigationException(f)

    finally:
      self.end_graciously(sTs, trough)
