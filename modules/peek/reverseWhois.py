#!/usr/bin/env python 3

from os import environ as env
from dotenv import load_dotenv
from json import dumps
from requests import post

from sessions.exceptions import AuthorisationException, QueryException

from phrases import exceptions as e
from src.globals import structures as st

load_dotenv()

W2_USER           = env.get('API_KEY_WHOISXML')
endpoint          = 'https://reverse-whois.whoisxmlapi.com/api/v2'
RESULTS_CAP       = env.get('DEFAULT_REVERSE_WHOIS_QUERY_RESULTS_CAP')

def make_pretty(target, response):
  _dict                   = response.json()
  amount                  = _dict['domainsCount']
  next_page_search_after  = _dict['nextPageSearchAfter']
  output                  = ''

  if amount > 0:
    output               += f'WhoisXMLApi found {str(amount)} domain results:\n\n'
    i                     = 0

    for entry in _dict['domainsList']:
      i                   = i+1
      output             += f'  * {entry}\n'

      if RESULTS_CAP is not None and i == int(RESULTS_CAP):
        output           += f'\n Skipped output of {amount - i} other entries.\n'
        break

  else:
    output               += f'WhoisXMLApi found no domain results for {target}.'
  if next_page_search_after is not None:
    output               += f'Next search after: {next_page_search_after}'

  print(output)

def clean_list(_list):
  l = len(_list)
  cleaned_list = []

  for i in range(l):
    member      = _list[i-1]
    member      = member.strip(' ')
    cleaned_list.insert(i-1, member)

  return cleaned_list

def retrieve(target, **options):
  timestamp     = ''
  _options      = options.get('options')
  searchType    = 'current'

  if 'constants' in _options.keys() and 'HISTORIC' in _options['constants']:
    searchType  = 'historic'

  targets       = target.strip('\'" ')
  targets       = targets.split(' NOT ')
  wanted        = targets.pop(0)
  unwanted      = targets
  wanted        = wanted.split(' AND ')

  if unwanted is None:
    unwanted    = []

  unwanted      = clean_list(unwanted)
  wanted        = clean_list(wanted)
  max_amount    = 4
  LIMIT         = max_amount
  n_excludes    = []
  n_includes    = []

  if len(unwanted) > LIMIT:
    excludes    = unwanted[:LIMIT]

    for item in excludes:
      unwanted.remove(item)

    n_excludes  = unwanted

  elif len(unwanted) == 0:
    excludes    = []
  else:
    excludes    = unwanted

  if len(wanted) > LIMIT:
    includes    = wanted[:LIMIT]

    for item in includes:
      wanted.remove(item)

    n_includes  = wanted

  else:
    includes    = wanted

  print(f'Included terms: {str(includes)}')
  if len(excludes) > 0:
    print(f'Excluded terms: {str(excludes)}')
  if len(n_includes) > 0:
    print(f'Max of {max_amount} terms exceeded. Dropped terms from inclusion: {str(n_includes)}')
  if len(n_excludes) > 0:
    print(f'Max of {max_amount} exclusion terms exceeded. Dropped terms from exclusion: {str(n_excludes)}')

  data          = {
    'apiKey'      : W2_USER,
    'searchType'  : searchType,
    'mode'        : 'purchase',
    'punycode'    : True,
    'searchAfter' : timestamp,
    'basicSearchTerms': {
      'include'   : includes,
      'exclude'   : excludes
    }
  }

  if 'prepositions' in _options.keys():
    prepos_options  = _options['prepositions']

    for key in prepos_options:
      prepos_key    = key
      prepos_value  = prepos_options[key]

    if prepos_key == 'before' or prepos_key == 'after':
      _map = {
        'before' : 'createdDateTo',
        'after'  : 'createdDateFrom'
      }
      _dict = { _map[prepos_key] : prepos_value[0] }
      data.update(_dict)
      print(f'Querying for records {prepos_key} : {prepos_value[0]}')

    elif prepos_key == 'between':
      from_to = prepos_value
      _dict = {
        'createdDateFrom' : from_to[0],
        'createdDateTo'   : from_to[1]
      }
      data.update(_dict)
      print(f'Querying for records {prepos_key} : {from_to[0]} and {from_to[1]}')

  print(st['glorious_separation'])

  data          = dumps(data)

  try:
    response    = post(endpoint, data=data)

  except Exception as f:
    raise QueryException(f'{e.query_whoisxmlapi_failed}: {f}.')

  return response

def whoisQuery(trough, *args, **options):
  target      = args[0]

  if W2_USER is not None:
    try:
      result  = retrieve(target, **options)
      sc      = result.status_code

      if sc == 200:
        try:
          make_pretty(target, result)
        except Exception as f:
          raise f

      elif sc == 401 or sc == 422:
        print(result.text, result.status_code)
      else:
        raise QueryException(f'{e.query_whoisxmlapi_failed}: Status not OK, but {sc}.')

    except Exception as f:
      raise f

  else:
    raise AuthorisationException(f'{e.query_whoisxmlapi_failed}: WhoisXMLAPI key missing.')

  return trough
