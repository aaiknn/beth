#!/usr/bin/env python3

from os import environ as env
from dotenv import load_dotenv

from json import dumps
from requests import post

load_dotenv()
US_USER   = env.get('API_KEY_URLSCAN')

_dict = None

class UsRecord:
  def __init__(self, api, country, message, options, result, url, uuid, visibility):
    self.api            = api
    self.country        = country
    self.message        = message
    self.options        = options
    self.result         = result
    self.url            = url
    self.uuid           = uuid
    self.visibility     = visibility

class UsResponse:
  def __init__(self, response):
    self.entry  = UsRecord(
      response['api'],
      response['country'],
      response['message'],
      response['options'],
      response['result'],
      response['url'],
      response['uuid'],
      response['visibility']
    )

def make_pretty(response):
  _dict       = UsResponse(response.json())
  output      = ""
  output      += _dict.entry.message
  output      += ": "
  output      += _dict.entry.result
  output      += " ("
  output      += _dict.entry.url
  output      += ")."

  return output

def scan_submission(target):
  headers     = {'API-Key':str(US_USER),'Content-Type':'application/json'}
  data        = {"url": target, "visibility": "public"}
  response    = post('https://urlscan.io/api/v1/scan/',headers=headers, data=dumps(data))

  return response

def scan(target):
  if US_USER is not None:
    response = scan_submission(target)
    print(make_pretty(response))
  else:
    return
