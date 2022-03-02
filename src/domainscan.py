#!/usr/bin/env python3

from os import environ as env
from dotenv import load_dotenv
from json import dumps
from requests import post

from sessions.exceptions import AuthorisationException
from utils.renderers.UrlscanResponse import UsMessage, UsResponse

load_dotenv()
US_USER   = env.get('API_KEY_URLSCAN')

_dict = None

def make_pretty(response):
  try:
    _dict       = UsResponse(response.json())
    output      = ""
    output      += _dict.entry.message
    output      += ": "
    output      += _dict.entry.result
    output      += " ("
    output      += _dict.entry.url
    output      += ")."

  except Exception as f:
    raise f

  print(output)

def scan_submission(target):
  headers     = {'API-Key':str(US_USER),'Content-Type':'application/json'}
  data        = {"url": target, "visibility": "public"}
  response    = post('https://urlscan.io/api/v1/scan/',headers=headers, data=dumps(data))

  return response

def scan(trough, *args, **options):
  if US_USER is not None:
    try:
      response  = scan_submission(args[0])
      sc        = response.status_code

    except Exception as f:
      raise f

    if sc == 200:
      try:
        make_pretty(response)

      except Exception as f:
        raise f

    else:
      m       = response.json()
      result  = UsMessage(
        args[0],
        sc,
        m['message']
      )
      print(f'Response code {result.result}: {result.message} ({result.url}).')

  else:
    raise AuthorisationException(f'')

  return trough
