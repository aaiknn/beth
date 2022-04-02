#!/usr/bin/env python3

from os import environ as env
from dotenv import load_dotenv
from requests import get

from utils.renderers.whoisxmlapi.whoisRenderer import WhoisResponse as WXAResponse
from utils.renderers.whoxy.whoisRenderer import WhoisResponse as WxyResponse
from sessions.exceptions import AuthorisationException, QueryException, UnsuccessfulQueryWarning

from phrases import exceptions as e

load_dotenv()

WHOIS_SERVICE = env.get('DEFAULT_WHOIS_SERVICE')
if WHOIS_SERVICE == 'WHOISXMLAPI':
  WHOIS_USER    = env.get('API_KEY_WHOISXML')
  ENDPOINT      = 'https://www.whoisxmlapi.com/whoisserver/WhoisService'
elif WHOIS_SERVICE == 'WHOXY':
  WHOIS_USER    = env.get('API_KEY_WHOXY')
  ENDPOINT      = 'http://api.whoxy.com/'
else:
  WHOIS_SERVICE = None
  WHOIS_USER    = None
  ENDPOINT      = None

def make_pretty(response):
  if WHOIS_SERVICE == 'WHOISXMLAPI':
    response = WXAResponse(response)
  elif WHOIS_SERVICE == 'WHOXY':
    response = WxyResponse(response)

  response.render()

def retrieve(target):
  try:
    if WHOIS_SERVICE == 'WHOISXMLAPI':
      response = get(f'{ENDPOINT}?apiKey={WHOIS_USER}&domainName={target}&outputFormat=JSON')
    elif WHOIS_SERVICE == 'WHOXY':
      response = get(f'{ENDPOINT}?key={WHOIS_USER}&whois={target}')

  except Exception as f:
    raise QueryException(f'{e.query_whois_failed}: {f}.')

  return response

def whoisQuery(trough, *args, **options):
  if WHOIS_SERVICE is not None:
    if WHOIS_USER is not None:
      try:
        result  = retrieve(args[0])
        sc      = result.status_code

        if sc == 200:
          try:
            make_pretty(result)

          except UnsuccessfulQueryWarning as f:
            print(f)

          except Exception as f:
            raise f

        elif sc == 401:
          print(result.text, result.status_code)

        else:
          raise QueryException(f'{e.query_whoisxmlapi_failed}: Status not OK, but {sc}.')

      except Exception as f:
        raise f

    else:
      raise AuthorisationException(f'{e.query_whoisxmlapi_failed}: WhoisXMLAPI key missing.')
  else:
    raise Exception('NoWhoisServiceWarning')

  return trough
