#!/usr/bin/env python3

from os import environ as env
from dotenv import load_dotenv
from json import dumps, loads
from requests import get, post
from time import sleep

from sessions.exceptions import AuthorisationException, RenderException, SubmissionException
from utils.renderers.urlscan.UrlscanSubmissionResponse import UrlscanResponse
from utils.renderers.urlscan.UrlscanScanResultResponse import UrlscanResponse as ScanResponse

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

def scan(*args, **options):
  if US_USER is None:
    raise AuthorisationException(f'{e.query_urlscan_failed}: Urlscan API key is missing.')

  target = args[0]

  try:
    response  = scan_submission(target)
  except Exception as f:
    raise SubmissionException(f)

  try:
    _dict       = UrlscanResponse(response, target)
    _dict.render()

  except Exception as f:
    raise RenderException(f)

  jobData = response.json()
  return jobData

def retrieve_scan_results(url, target):
  sleep(7)
  response  = get(url)
  if response.status_code == 200:
    _dict   = ScanResponse(response, target)

    if len(_dict.requests) > 0:
      output      = '\n'
      output     += str(len(_dict.requests))
      output     += ' requests:\n'

      for entry in _dict.requests:
        e_keys    = entry.keys()
        failed    = entry['response_failed']

        if 'failed':
          errorText = entry['response_error_text']
          output   += f'Request failed: {errorText}.'
        else:
          e_url     = entry['response_url']
          output   += f'* {e_url}'

          if 'response_ip' in entry.keys() and 'response_port' in entry.keys():
            e_ip    = entry['response_ip']
            e_port  = entry['response_port']
            output += f' ({e_ip}:{e_port})\n'
          else:
            output += '\n'

      print(output)

    return _dict
  else:
    retrieve_scan_results(url, target)

def full_scan(*args, **options):
  target    = args[0]
  jobData   = scan(*args, **options)
  endpoint  = jobData['api']

  print('Waiting to retrieve scan results...')
  _dict = retrieve_scan_results(endpoint, target)
  return _dict
