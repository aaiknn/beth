#!/usr/bin/env

from os import environ as env
from dotenv import load_dotenv
from requests import get
from requests.exceptions import ConnectionError

load_dotenv()

USER_AGENT  = env.get('DEFAULT_USER_AGENT')

def handleResponse(response):
  sc      = str(response.status_code)
  _map    = {
    '200' : 'Target reachable',
    '203' : 'None-authoritative information',
    '301' : 'Target is redirecting',
    '405' : 'Method disallowed. Domain may be controlled.',
    '522' : 'Web server unreachable'
  }

  if sc in _map.keys():
    print(sc, _map[sc])
  else:
    print(f'Not in map: {response.status_code}, {response.text}')

  if sc == '203':
    print(response.text)

def sendRequest(url):
  if USER_AGENT is None:
    AGENT = 'BETH_FROM_ABOVE'
  else:
    AGENT = USER_AGENT

  headers = {
    'User-Agent': str(AGENT)
  }

  try:
    response = get(url, headers=headers)
  except Exception as f:
    raise(f)

  return response

def identifyTarget(target):
  target = target.split('//')

  if len(target) > 1:
    target = f'{target[0]}//{target[1]}'
  else:
    target = f'http://{target[0]}'

  return target

def is_it_up(trough, *args, **options):
  target = args[0]
  target = identifyTarget(target)

  try:
    sendRequest(target)
  except ConnectionError as f:
    print(f'\033[31m{target} can\'t be reached.\033[0m')
  except Exception as f:
    raise(f)
  else:
    print(f'\033[32m{target} is up.\033[0m')

  return trough

def whats_the_status(trough, *args, **options):
  target = args[0]
  target = identifyTarget(target)

  try:
    response = sendRequest(target)
  except ConnectionError as f:
    print(f'\033[31m{target} can\'t be reached.\033[0m')
  except Exception as f:
    raise(f)
  else:
    handleResponse(response)

  return trough
