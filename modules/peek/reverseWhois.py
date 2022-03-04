#!/usr/bin/env python 3

from os import environ as env
from dotenv import load_dotenv
from json import dumps
from requests import post

from sessions.exceptions import AuthorisationException, QueryException

from phrases import exceptions as e

load_dotenv()

W2_USER           = env.get('API_KEY_WHOISXML')

endpoint  = 'https://reverse-whois.whoisxmlapi.com/api/v2'

def make_pretty(target, response):
  _dict                   = response.json()
  amount                  = _dict['domainsCount']
  next_page_search_after  = _dict['nextPageSearchAfter']
  output                  = ''

  if amount > 0:
    output               += f'WhoisXMLApi found {str(amount)} domain results:\n\n'

    for entry in _dict['domainsList']:
      output             += f'  * {entry}\n'
  else:
    output               += f'WhoisXMLApi found no domain results for {target}.'

  if next_page_search_after is not None:
    output               += f'Next search after: {next_page_search_after}'

  print(output)

def retrieve(target):
  timestamp   = ''
  data        = {
    'apiKey': W2_USER,
    'searchType': 'historic',
    'mode': 'purchase',
    'punycode': True,
    'searchAfter': timestamp,
    'basicSearchTerms': {
      'include': [
        target
      ],
      'exclude': []
    }
  }
  data        = dumps(data)

  try:
    response = post(endpoint, data=data)

  except Exception as f:
    raise QueryException(f'{e.query_whoisxmlapi_failed}: {f}.')

  return response

def whoisQuery(trough, *args, **options):
  target      = args[0]

  if W2_USER is not None:
    try:
      result  = retrieve(target)
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
