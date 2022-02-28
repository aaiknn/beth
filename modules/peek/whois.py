#!/usr/bin/env python 3

from os import environ as env
from dotenv import load_dotenv
from requests import get

from sessions.exceptions import AuthorisationException, QueryException, UnsuccessfulQueryWarning

from phrases import exceptions as e

load_dotenv()

W2_USER           = env.get('API_KEY_WHOISXML')

endpoint  = 'https://www.whoisxmlapi.com/whoisserver/WhoisService'

def make_pretty(response):
  _dict             = response.json()
  _dict             = _dict['WhoisRecord']
  _keys             = _dict.keys()

  fqdm              = _dict['domainName']

  w_code            = _dict['parseCode']
  r_w_server        = 'NOT STATED'

  if 'registryData' in _keys:
    if 'whoisServer' in _dict['registryData'].keys():
      r_w_server    = _dict['registryData']['whoisServer']

  if w_code == 0:
    ext_message     = _dict['registryData']['rawText']

    eff             = f'{e.query_whoisxmlapi_unsucessful} for {fqdm}\n'

    if 'dataError' in _keys:
      err_message   = _dict['dataError']
      eff          += f'Code {w_code}: {err_message}\n'
    else:
      eff          += f'Code {w_code}: Bad entry.\n'

    if 'registrarName' in _keys and r_w_server != 'NOT STATED':
      eff          += f'\nResponsible whois server: {r_w_server}\n'

    if ext_message is not None:
      eff          += f'\n{ext_message}\n'

    raise UnsuccessfulQueryWarning(eff)

  tld               = _dict['domainNameExt']

  w_c_date          = _dict['audit']['createdDate']
  w_u_date          = _dict['audit']['updatedDate']

  e_age             = _dict['estimatedDomainAge']

  r_name            = _dict['registrarName']
  r_status          = _dict['registryData']['status']
  r_code            = _dict['registryData']['parseCode']
  r_date_created    = _dict['registryData']['createdDateNormalized']
  r_date_expires    = _dict['registryData']['expiresDateNormalized']
  r_date_updated    = _dict['registryData']['updatedDateNormalized']
  r_ns              = _dict['registryData']['nameServers']['hostNames']

  res_message       = ''
  res_message      += f'Registrar       : {r_name}\n'
  res_message      += f'Status          : {r_status}\n'
  res_message      += f'Parse code      : {r_code}\n\n'

  if len(r_ns) >= 1:
    res_message    += f'Nameservers     :\n'

    for entry in r_ns:
      res_message  += f'  * {entry}\n'

  res_message      += f'\nImportant dates :\n'
  res_message      += f'Record expires  : {r_date_expires}\n'
  res_message      += f'Record created  : {r_date_created}\n'
  res_message      += f'Record updated  : {r_date_updated}\n\n'

  print(res_message)

def retrieve(target):
  try:
    response = get(f'{endpoint}?apiKey={W2_USER}&domainName={target}&outputFormat=JSON')
  except Exception as f:
    raise QueryException(f'{e.query_whoisxmlapi_failed}: {f}.')

  return response


def whoisQuery(target):
  if W2_USER is not None:
    result  = retrieve(target)
    sc      = result.status_code

    if sc == 200:
      try:
        make_pretty(result)
      except UnsuccessfulQueryWarning as f:
        print(f)
    else:
      raise QueryException(f'{e.query_whoisxmlapi_failed}: Status not OK, but {sc}.')

  else:
    raise AuthorisationException(f'{e.query_whoisxmlapi_failed}: WhoisXMLAPI key missing.')
