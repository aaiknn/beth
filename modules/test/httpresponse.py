#!/usr/bin/env

from os import environ as env, path
from fileinput import input
from dotenv import load_dotenv
from requests import get

from requests.exceptions import ConnectionError, HTTPError
from sessions.exceptions import NoTargetWarning

from src.globals import structures as st

load_dotenv()

USER_AGENT            = env.get('DEFAULT_USER_AGENT')
STATUS_TELL_ME_MORES  = env.get('DEFAULT_HTTP_STATUS_TELL_ME_MORES')

if STATUS_TELL_ME_MORES is None:
  STATUS_TELL_ME_MORES = []

def prettifyHeaders(headers):
  _dict               = headers
  _keys               = _dict.keys()

  for member in _keys:
    print(f'  {member} : {_dict[member]}')

def handleResponse(target, response):
  sc                  = str(response.status_code)
  response_map        = {
    '200' : 'Target reachable.',
    '203' : 'None-authoritative information.',
    '301' : 'Target is redirecting.'
  }
  funky_map           = {
    '403' : 'Target doesn\'t think you should come here.',
    '404' : 'Resource not found.',
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

  if sc in STATUS_TELL_ME_MORES:
    try:
      prettifyHeaders(response.headers)
    except Exception as f:
      print(f)

def sendRequest(url):
  if USER_AGENT is None:
    headers = {}
  else:
    headers = {
      'User-Agent': str(USER_AGENT)
    }

  try:
    response = get(url, headers=headers)
  except Exception as f:
    raise(f)

  return response

def handle_request(loc, _dict, mode):
  try:
    response, _dict  = handle_or_retrieve(loc, _dict)
  except KeyboardInterrupt as stahp:
    raise stahp
  except NoTargetWarning:
    print('Skipping empty line.')

  except HTTPError as f:
    c  = 'UNKNOWN'
    m  = f'\033[31m{loc}\033[0m can\'t be reached.'
    if mode != 'up':
      c  = 'X00'
      m  = f'[-] ' + m + f'({f})'
    print(m)
    _dict = update_summary(_dict, c, loc)

  except ConnectionError as f:
    c = 'DOWN'
    m = f'\033[31m{loc}\033[0m can\'t be reached.'
    if mode != 'up':
      c = 'X01'
      m = f'[-] ' + m
    print(m)
    _dict = update_summary(_dict, c, loc)

  except Exception as f:
    _dict = update_summary(_dict, 'ERROR', loc)
    raise Exception(f)
  else:
    if mode == 'up':
      print(f'\033[32m{loc}\033[0m is up.')
      _dict = update_summary(_dict, 'UP', loc)
    else:
      handleResponse(loc, response)

  return _dict

def identifyTarget(target):
  target            = target.split('//')
  if len(target) > 1:
    target          = f'{target[0]}//{target[1]}'
  else:
    target          = f'http://{target[0]}'
  return target

def sanitiseLine(line):
  if len(line) == 0:
    raise NoTargetWarning()
  elif line.startswith('#') or line.startswith('//'):
    raise NoTargetWarning()

  return line

def handle_or_retrieve(loc, _dict):
  try:
    loc           = sanitiseLine(loc)
    target        = identifyTarget(loc)
    response      = sendRequest(target)
  except Exception as f:
    raise f
  else:
    sc = str(response.status_code)
    _dict = update_summary(_dict, sc, target)

  return (response, _dict)

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

def update_summary(_dict, sc, target):
  if sc in _dict.keys():
    _dict[sc].append(target)
  else:
    _dict.update({ sc : [ target ] })

  return _dict

def summarise(_dict):
  _keys             = _dict.keys()
  _output           = ''
  _output          += st['glorious_separation']
  _output          += '\nSUMMARY:\n'
  _output          += st['glorious_separation']

  _output          += '\nAmounts:\n\n'

  for entry in _keys:
    amount          = len(_dict[entry])
    _output        += f' * {entry}: {amount}\n'

  _output        += '\nEntries:\n\n'

  for entry in _keys:
    amount          = len(_dict[entry])
    _output        += f'{entry}s ({amount}):\n'

    for member in _dict[entry]:
      _output      += f' * {member}\n'

  print(_output)

def is_it_up(*args, **options):
  input           = args[0]

  try:
    _data   = prepData(input, **options)
  except Exception as f:
    raise Exception(f)
  else:
    _dict         = {}
    for member in _data:
      _dict = handle_request(member, _dict, 'up')

  finally:
    summarise(_dict)
    return None

def whats_the_status(*args, **options):
  input           = args[0]

  try:
    _data         = prepData(input, **options)
  except Exception as f:
    raise Exception(f)
  else:
    _dict         = {}
    for member in _data:
      _dict = handle_request(member, _dict, 'status')

  finally:
    summarise(_dict)
    return None
