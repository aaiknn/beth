#!/usr/bin/env python3

from os import environ as env
from dotenv import load_dotenv
from json import dumps, loads
from requests import post

from sessions.exceptions import AuthorisationException
from utils.renderers.urlscan.UrlscanSubmissionResponse import UrlscanResponse

from phrases import exceptions as e

load_dotenv()
US_USER       = env.get('API_KEY_URLSCAN')
DEFAULT_TAGS  = env.get('DEFAULT_URLSCAN_SCAN_TAGS')

def scan_submission(target):
  headers     = {
    'API-Key'       : str(US_USER),
    'Content-Type'  : 'application/json'
  }
  data        = {
    'url'           : target,
    'visibility'    : 'public'
  }

  if DEFAULT_TAGS is not None:
    try:
      tags = loads(DEFAULT_TAGS)
    except:
      raise ValueError('DEFAULT_URLSCAN_SCAN_TAGS environment variable is formatted incorrectly.')

    if len(tags) > 0:
      _dict = { 'tags' : tags }
      data.update(_dict)

  data        = dumps(data)

  response    = post(
    'https://urlscan.io/api/v1/scan/',
    headers = headers,
    data    = data
  )
  return response

def scan(trough, *args, **options):
  if US_USER is None:
    raise AuthorisationException(f'{e.query_urlscan_failed}: Urlscan API key is missing.')

  target = args[0]

  try:
    response  = scan_submission(target)
    sc        = response.status_code
  except Exception as f:
    raise f

  try:
    _dict       = UrlscanResponse(response, target)
    _dict.render()

  except Exception as f:
    raise f

  return trough
