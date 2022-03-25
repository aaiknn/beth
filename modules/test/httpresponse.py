#!/usr/bin/env

from os import environ as env, path
from fileinput import input
from dotenv import load_dotenv
from requests import get
from requests.exceptions import ConnectionError

from sessions.exceptions import NoTargetWarning

load_dotenv()

USER_AGENT            = env.get('DEFAULT_USER_AGENT')

def prettifyHeaders(headers):
  _dict               = headers
  _keys               = _dict.keys()

  for member in _keys:
    print(f'  {member} : {_dict[member]}')

def handleResponse(target, response):
  sc                  = str(response.status_code)
  tell_me_mores       = ['200', '203', '301', '503']
  response_map        = {
    '200' : 'Target reachable.',
    '203' : 'None-authoritative information.',
    '301' : 'Target is redirecting.'
  }
  funky_map           = {
    '403' : 'Target doesn\'t think you should come here.',
    '405' : 'Method disallowed. Domain may be controlled.',
    '500' : 'Internal server error.',
    '502' : 'Bad gateway.',
    '503' : 'Service unavailable.',
    '521' : 'Web server is down.',
    '522' : 'Connection timed out.',
    '523' : 'Origin is unreachable.',
    '526' : 'Invalid SSL certificate. (And possibly for a reason.)'
  }

  if sc in response_map.keys():
    print(f'[+] \033[32m{sc}\033[0m {target} : {response_map[sc]}')
  elif sc in funky_map.keys():
    print(f'[-] \033[33m{sc}\033[0m {target} : {funky_map[sc]}')
  else:
    print(f'[!] \033[33m{sc}\033[0m {target} :\n{response.text}')

  if sc in tell_me_mores:
    try:
      prettifyHeaders(response.headers)
    except Exception as f:
      print(f)

def summarise(_dict, **options):
  _keys             = _dict.keys()
  _output           = ''

  _output          += 'Summary:\n\n'

  for entry in _keys:
    _output        += f'{entry}s:\n'
    for member in entry:
      _output      += f'  * {member}\n'

  print(_output)

def sendRequest(url):
  if USER_AGENT is None:
    AGENT           = 'BETH_FROM_ABOVE'
  else:
    AGENT           = USER_AGENT

  headers = {
    'User-Agent': str(AGENT)
  }

  try:
    response = get(url, headers=headers)
  except Exception as f:
    raise(f)

  return response

def sanitiseLine(line):
  if len(line) == 0:
    raise NoTargetWarning()
  elif line.startswith('#') or line.startswith('//'):
    raise NoTargetWarning()

  return line

def identifyTarget(target):
  target            = target.split('//')

  if len(target) > 1:
    target          = f'{target[0]}//{target[1]}'
  else:
    target          = f'http://{target[0]}'

  return target

def prepData(_input, **options):
  _data             = []
  _options          = options.get('options')

  if 'constants' in _options.keys() and 'BULK_FILE' in _options['constants']:
    if path.exists(_input):
      with input(files=(_input)) as doc:
        for entry in doc:
          entry     = entry.split('\n')
          entry     = entry[0]
          _data.append(entry)

    else:
      raise FileNotFoundError(f'\'{_input}\' doesn\'t appear to be an existing path on your system.')

  else:
    _data.append(_input)

  return _data

def handle_or_retrieve(loc):
  try:
    loc           = sanitiseLine(loc)
    target        = identifyTarget(loc)
    response      = sendRequest(target)
  except Exception as f:
    raise f
  else:
    return response

def is_it_up(trough, *args, **options):
  input           = args[0]
  _dict           = {}

  try:
    _data   = prepData(input, **options)
  except Exception as f:
    raise Exception(f)

  else:
    for member in _data:
      try:
        response  = handle_or_retrieve(member)
      except NoTargetWarning as eh:
        print('Skipping empty line.')
        continue
      except ConnectionError as f:
        print(f'\033[31m{member} can\'t be reached.\033[0m')
        sc        = 'X01'
      except Exception as f:
        sc        = 'X02'
        raise Exception(f)
      else:
        print(f'\033[32m{member} is up.\033[0m')
        sc        = str(response.status_code)

  finally:
    return trough

def whats_the_status(trough, *args, **options):
  input           = args[0]

  try:
    _data         = prepData(input, **options)
  except Exception as f:
    raise Exception(f)

  else:
    for member in _data:
      try:
        response  = handle_or_retrieve(member)
      except ConnectionError as f:
        print(f'[-] \033[31m{member}\033[0m can\'t be reached.')
      except NoTargetWarning as eh:
        print('Skipping empty line.')
        continue
      except Exception as f:
        raise Exception(f)
      else:
        handleResponse(member, response)

  finally:
    return trough
