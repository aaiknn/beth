#!/usr/bin/env python3

from time import sleep
from os import environ as env
from dotenv import load_dotenv
from requests import get

from avionics.environmentals import SenseOfTime
from sessions.exceptions import AuthorisationException, QueryException, UnreachableException
from utils.trough.TroughObject import UrlscanQueryResultTroughObject as UsTO

from phrases import exceptions as e

load_dotenv()

US_USER           = env.get('API_KEY_URLSCAN')
DEFAULT_AMOUNT    = env.get('DEFAULT_URLSCAN_QUERY_RESULTS_AMOUNT')
DEFAULT_INTERVAL  = env.get('DEFAULT_URLSCAN_QUERY_INTERVAL')

nav               = SenseOfTime()

def make_pretty(response):
  _dict         = response.json()
  res_amount    = len(_dict['results'])
  max_amount    = _dict['total']
  i             = 1
  _all          = []

  nav.state_time()
  print(f'Total results: {max_amount}\nDisplaying {res_amount}.\n')

  for entry in _dict['results']:
    i_date        = entry['indexedAt']
    _date         = str(i_date)
    r_keys        = entry.keys()

    fqdm          = entry['task']['domain']
    t_keys        = entry['task'].keys()

    s_req_amount  = entry['stats']['requests']

    print(f'{i} - {_date}: \033[33m{fqdm}\033[0m')

    if 'page' in r_keys:
      p_asnn          = entry['page']['asnname']
      p_asn           = entry['page']['asn']
      p_ip            = entry['page']['ip']
      p_url           = entry['page']['url']
      p_status        = entry['page']['status']

      print(f'  Effective URL: {p_url} ({p_status}) - {s_req_amount} requests')

      if fqdm not in _all:
        print(f'  ASN {p_asn} ({p_asnn}): {p_ip}')

        if 'result' in r_keys:
          r_result        = entry['result']
          print(f'  Scan response location: {r_result}')

        if 'screenshot' in r_keys:
          r_screenshot    = entry['screenshot']
        print(f'  Website screenshot location: {r_screenshot}')

    if 'tags' in t_keys:
      _tags     = entry['task']['tags']
      output    = ''

      for _tag in _tags:
        output += f'\033[36m{_tag}\033[0m'
        output += ', '

      print(f'  Tags: {output[:-2]}')

    if fqdm not in _all:
      _all.append(fqdm)

    i = i+1

def retrieve(*args):
  term            = args[0]

  if len(args) == 1:
    size          = DEFAULT_AMOUNT
  elif len(args) >= 1:
    size          = str(args[1])

  try:
    headers     = {'API-Key':str(US_USER),'Content-Type':'application/json'}
    response    = get(f'https://urlscan.io/api/v1/search/?q={term}&size={size}',headers=headers)
  except Exception as f:
    raise UnreachableException(f'{e.query_urlscan_failed}: {f}')

  return response

def save_unique_to_trough(response, trough):
  _dict       = response.json()
  _array      = []
  _positions  = []

  i = 0

  for entry in _dict['results']:
    if entry['page']['domain'] not in _array:
      _positions.append(i)
      _array.append(entry['page']['domain'])

    i = i+1
  
  print(f'\n{len(_array)} unique domains:')

  for index in _positions:
    result  = _dict['results'][index]
    fqdm    = result['task']['domain']
    to      = UsTO(result)
    trough.data.append(to)
    print(f'  * {fqdm}')

def query(trough, *args, **options):
  _options    = options.get('options')

  if US_USER is not None:
    response  = retrieve(*args)
    sc        = response.status_code

    if sc == 200:
      make_pretty(response)
      save_unique_to_trough(response, trough)
    elif sc == 429:
      raise QueryException(f'{e.query_urlscan_failed}: Urlscan rate limit reached.')
    else:
      raise QueryException(f'{e.query_urlscan_failed}: Status not OK, but {sc}.')

  else:
    raise AuthorisationException(f'{e.query_urlscan_failed}: Urlscan API key missing.')

  if _options == 'REPEAT':
    try:
      sleep(int(DEFAULT_INTERVAL))
    except KeyboardInterrupt:
      return
    except:
      sleep(900)
    finally:
      query(*args, **options)

  return trough
