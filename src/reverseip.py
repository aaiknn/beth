#!/usr/bin/env python3

from os import environ as env
from dotenv import load_dotenv
from ipaddress import ip_address
from requests import post

from sessions.exceptions import AuthorisationException

from phrases import exceptions as e

load_dotenv()

ST_USER   = env.get('API_KEY_SECURITY_TRAILS')
_dict     = None

class StRecord:
  def __init__(self, hostname, host_provider, mail_provider, registrar, created, expires, company):
    self.hostname       = hostname
    self.host_provider  = host_provider
    self.mail_provider  = mail_provider
    self.registrar      = registrar
    self.created        = created
    self.expires        = expires
    self.company        = company

class StResponse:
  def __init__(self, response):
    self.obj            = response
    self.reduced        = []

    if self.obj['records']:
      try:
        self.records    = self.obj['records']
        self.amount     = self.obj['record_count']
        self.meta       = self.obj['meta']

      except Exception as f:
        raise f

      for record in self.records:
        entry = StRecord(
          record['hostname'],
          record['host_provider'],
          record['mail_provider'],
          record['whois']['registrar'],
          record['whois']['createdDate'],
          record['whois']['expiresDate'],
          record['computed']['company_name']
        )
        self.reduced.append(entry)

    elif self.obj['message']:
      self.message  = self.obj['message']
      self.reduced.append(self.message)

def validate(target):
  try:
    ip_type = ip_address(target)

  except Exception as f:
    f_name = str(type(f).__name__)
    print(f_name, ':', f)
    raise f

  else:
    return ip_type.version

def pull(ip_version, target):
  endpoint    = 'https://api.securitytrails.com/v1/domains/list?include_ips=false&page=1&scroll=false'
  headers     = {
    "Content-Type": "application/json",
    "APIKEY": str(ST_USER)
  }
  filter      = "ipv" + str(ip_version)
  data        = {"filter": {filter: target}}

  try:
    response  = post(endpoint, json=data, headers=headers)

  except Exception as f:
    f_name = str(type(f).__name__)
    print(f_name, ':', f)
    raise f

  return response

def clean_up(response):
  result = StResponse(response)
  return result

def make_pretty(obj_list):
  i             = 0
  output        = ""

  for entry in obj_list:
    i           = i+1

    if entry.hostname is not None:
      output   += "\n\n"
      output   += str(i)
      output   += ".\nHost name: "
      output   += entry.hostname

    if entry.host_provider is not None:
      output   += "\n"
      output   += "Host providers: "

      for item in entry.host_provider:
        output += str(item)
        output += ", "

    if entry.mail_provider is not None:
      output   += "\n"
      output   += "Mail providers: "

      for item in entry.mail_provider:
        output += str(item)
        output += ", "

    if i == 20 and len(obj_list) > 20:
      output   += f'\n\nSkipped output of {len(obj_list) - i} other items.'
      break

  if len(obj_list) == 1:
    output     += str(obj_list[0])

  print(output)

def reverse(trough, *args, **options):
  try:
    ip_version = validate(args[0])

  except Exception as f:
    raise f

  if ST_USER is not None:
    try:
      response = pull(ip_version, args[0])

    except Exception as f:
      raise f

    try:
      result = clean_up(response.json())
      make_pretty(result.reduced)

    except Exception as f:
      f_name = str(type(f).__name__)
      print(f_name, ':', f, '\n\n')
      print(str(response.text))

  else:
    raise AuthorisationException(f'{e.reverseip_securitytrails_failed}: SecurityTrails API key missing.')

  return trough
