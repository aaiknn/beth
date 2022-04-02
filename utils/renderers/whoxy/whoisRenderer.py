#!/usr/bin/env python3

from sessions.exceptions import UnsuccessfulQueryWarning
from phrases import exceptions as e

class WhoisResponse():
  def __init__(self, response):
    self.response = response
    self._dict    = response.json()

  def render(self):
    if self._dict['status'] != 1:
      if self._dict['status'] == 0:
        reason    = self._dict['status_reason']
        eff       = ''
        eff      += f'{e.query_whoxy_unsucessful}: {reason}.'
        raise UnsuccessfulQueryWarning(eff)
      else:
        print(self._dict)
    else:
      _keys               = self._dict.keys()
      fqdm                = self._dict['domain_name']
      r_w_server          = self._dict['whois_server']
      registered          = self._dict['domain_registered']
      res_message         = ''

      if str.lower(registered) == 'yes':
        is_registered     = True
      elif str.lower(registered) == 'no':
        is_registered     = False
      else:
        is_registered     = f'unknown ({registered})'

      try:
        if is_registered:
          res_message      += f'Registrar :\n'
          for entry in self._dict['domain_registrar']:
            value           = self._dict['domain_registrar'][entry]
            res_message    += f' {entry} : {value}\n'

          if 'domain_status' in _keys:
            res_message      += f'\nStatus :\n'
            for entry in self._dict['domain_status']:
              res_message  += f' * {entry}\n'

          if 'create_date' in _keys or 'update_date' in _keys or 'expiry_date' in _keys:
            res_message    += f'\nImportant dates :\n'
            if 'create_date' in _keys:
              _date         = self._dict['create_date']
              res_message  += f' Record created : {_date}\n'
            if 'expiry_date' in _keys:
              _date         = self._dict['expiry_date']
              res_message  += f' Record expires : {_date}\n'
            if 'update_date' in _keys:
              _date         = self._dict['update_date']
              res_message  += f' Record updated : {_date}\n'

          if 'name_servers' in _keys:
            res_message    += f'\nNameservers :\n'
            for entry in self._dict['name_servers']:
              res_message  += f' * {entry}\n'

          if 'registrant_contact' in _keys:
            the_guy         = self._dict['registrant_contact']
            res_message    += f'\n\nRegistrant data :\n'
            for entry in the_guy.keys():
              res_message  += f' {entry} : {the_guy[entry]}\n'

        elif not is_registered:
          print('Domain is not registered.\n')
          print(str(self._dict))
        else:
          print(f'Registration status: {is_registered}.')
          print(str(self._dict))

      except Exception as f:
        if 'raw_whois' in _keys:
          raw               = self._dict['raw_whois']
          print(raw)
        raise f

      print(res_message)
