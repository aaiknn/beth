#!/usr/bin/env python3
from sessions.exceptions import UnsuccessfulQueryWarning
from phrases import exceptions as e

class WhoisResponse():
  def __init__(self, response):
    self.response = response
    self._dict    = response.json()

  def render(self):
    _dict             = self._dict
    res_message       = ''

    if 'WhoisRecord' in _dict.keys():
      _dict           = _dict['WhoisRecord']
      _keys           = _dict.keys()
      fqdm            = _dict['domainName']
      w_code          = _dict['parseCode']
      r_w_server      = 'NOT STATED'

      if 'registryData' in _keys:
        if 'whoisServer' in _dict['registryData'].keys():
          r_w_server  = _dict['registryData']['whoisServer']

      if w_code == 0:
        eff               = f'{e.query_whoisxmlapi_unsucessful} for {fqdm}\n'

        if 'dataError' in _keys:
          err_message     = _dict['dataError']
          eff            += f'Code {w_code}: {err_message}\n'
        else:
          eff            += f'Code {w_code}: Bad entry.\n'

        if 'registrarName' in _keys and r_w_server != 'NOT STATED':
          eff            += f'\nResponsible whois server: {r_w_server}\n'

        if 'rawText' in _dict['registryData'].keys():
          ext_message     = _dict['registryData']['rawText']
          eff            += f'\n{ext_message}\n'

        raise UnsuccessfulQueryWarning(eff)

      tld                 = _dict['domainNameExt']
      w_c_date            = _dict['audit']['createdDate']
      w_u_date            = _dict['audit']['updatedDate']

      if 'estimatedDomainAge' in _keys:
        e_age             = _dict['estimatedDomainAge']

      r_name              = _dict['registrarName']

      res_message        += f'Registrar       : {r_name}\n'

      if 'registryData' in _keys:
        r_data            = _dict['registryData']
        _r_keys           = r_data.keys()

        if 'status' in _r_keys:
          r_status        = r_data['status']
          res_message    += f'Status          : {r_status}\n'

        r_code            = r_data['parseCode']
        res_message      += f'Parse code      : {r_code}\n'

        if 'createdDateNormalized' in _r_keys or 'expiresDateNormalized' in _r_keys or 'updatedDateNormalized' in _r_keys:
          res_message    += f'\nImportant dates :\n'

        if 'createdDateNormalized' in _r_keys:
          r_date_created  = r_data['createdDateNormalized']
          res_message    += f' Record created  : {r_date_created}\n'

        if 'expiresDateNormalized' in _r_keys:
          r_date_expires  = r_data['expiresDateNormalized']
          res_message    += f' Record expires  : {r_date_expires}\n'

        if 'updatedDateNormalized' in _r_keys:
          r_date_updated  = r_data['updatedDateNormalized']
          res_message    += f' Record updated  : {r_date_updated}\n'

        r_ns              = r_data['nameServers']['hostNames']

        if len(r_ns) >= 1:
          res_message    += f'\nNameservers     :\n'

          for entry in r_ns:
            res_message  += f' * {entry}\n'

      if 'registrant' in _keys:
        r_registrant    = _dict['registrant']
        r_r_keys        = r_registrant.keys()

        res_message    += f'\nRegistrant data :\n'

        for r_r_key in r_r_keys:
          res_message  += f' {r_r_key}: {r_registrant[r_r_key]}\n'

    else:
      res_message      += f'{self.response.text}'

    print(res_message)
