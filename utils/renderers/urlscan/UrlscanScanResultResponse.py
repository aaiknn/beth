#!/usr/bin/env python3

from sessions.exceptions import UnreachableException, RenderException

class UrlscanResponse:
  def __init__(self, response, target):
    self.target   = target
    self.response = response
    self._dict    = response.json()
    self.requests = []

    self.populate_requests()

  def populate_requests(self):
    _dict       = self._dict['data']
    requests    = _dict['requests']

    for entry in requests:
      e_request  = entry['request']
      e_response = entry['response']
      er_keys    = e_request.keys()
      re_keys    = e_response.keys()

      entryObj   = {
        'response_length' : e_response['dataLength']
      }

      if 'geoip' in er_keys:
        entryObj.update({
          'response_location' : e_response['geoip']
        })

      if 'request' in er_keys:
        entryObj.update({
          'url' : e_request['request']['url'],
          'method' : e_request['request']['method']
        })

      if 'hash' in re_keys:
        entryObj.update({
          'response_hash' : e_response['hash']
        })

      if 'remoteIPAddress' in re_keys and 'remotePort' in re_keys:
        entryObj.update({
          'response_ip' : e_response['remoteIPAddress'],
          'response_port' : e_response['remotePort']
        })

      if 'response' in re_keys:
        er_keys    = e_response['response'].keys()

        if 'failed' in re_keys:
          entryObj.update({
            'response_failed' : True,
            'response_error_text' : e_response['failed']['errorText'],
            'request_failed_url' : e_request['request']['url'],
            'request_failed_method' : e_request['request']['method']
          })

        else:
          if 'url' in er_keys:
            entryObj.update({
              'response_failed' : False,
              'response_url' : e_response['response']['url'],
              'response_status' : e_response['response']['status']
            })

          if 'responseTime' in er_keys:
            entryObj.update({
              'response_time' : e_response['response']['responseTime']
            })

          if 'securityDetails' in er_keys:
            sec        = e_response['response']['securityDetails']
            entryObj.update({
              'response_security_protocol' : sec['protocol'],
              'response_security_issuer' : sec['issuer'],
            })

      self.requests.append(entryObj)

  def render(self):
    try:
      output        = ""

      if 'data' in self._dict.keys():
        _dict       = self._dict['data']
        submitter   = self._dict['submitter']
        s_country   = submitter['country']
        requests    = _dict['requests']
        amount      = len(requests)

        output     += f'Scan submitted from {s_country}.\n\n'

        output     += f'{amount} HTTP request'
        if amount != 1:
          output   += 's'
        if amount != 0:
          output   += ':'
        else:
          output   += '.'

        for entry in requests:
          e_request  = entry['request']
          location   = e_request['documentURL']
          headers    = e_request['request']['headers']
          e_response = entry['response']

          if 'securityDetails' in e_response['response'].keys():
            sec        = e_response['response']['securityDetails']
            s_keys     = sec.keys()

          output   += f'\n\nDocument URL: {location}\n'
          output   += 'Request headers:\n'

          for key in headers.keys():
            value   = headers[key]
            output += f' * {key}: {value}\n'

          output   += '\nServer response:\n'

          for key in e_response.keys():
            value   = e_response[key]
            output += f' * {key}: {value}\n'

          if len(s_keys) > 0:
            output += '\nSecurity details:\n'
          for key in s_keys:
            value   = sec[key]

            if key == 'sanList':
              output += f'{key}:\n'
              for v in sec[key]:
                output += f' * {v}\n'
            else:
              output += f' * {key}: {value}\n'

      else:
        output     += 'Keys:\n'
        output     += self._dict.keys()

      print(output)

    except Exception as f:
      if self.response.status_code is None:
        raise UnreachableException(f'{f}: Response status code is None.')
      else:
        raise RenderException(f'Exception while trying to render response: {f}')
