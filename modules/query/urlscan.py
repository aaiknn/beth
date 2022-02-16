#!/usr/bin/env python3

from os import environ as env
from dotenv import load_dotenv

from requests import get

from sessions.exceptions import AuthorisationException, QueryException, UnreachableException
from phrases import exceptions as e

load_dotenv()

US_USER         = env.get('API_KEY_URLSCAN')
DEFAULT_AMOUNT  = env.get('DEFAULT_URLSCAN_QUERY_RESULTS_AMOUNT')

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

def query(*args):
  if US_USER is not None:
    response  = retrieve(*args)
    sc        = response.status_code

    if sc == 200:
      print(response.text)
    elif sc == 429:
      raise QueryException(f'{e.query_urlscan_failed}: Urlscan rate limit reached.')
    else:
      raise QueryException(f'{e.query_urlscan_failed}: Status not OK, but {sc}.')

  else:
    raise AuthorisationException(f'{e.query_urlscan_failed}: Urlscan API key missing.')
