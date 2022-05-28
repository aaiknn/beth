#!/usr/bin/env python3

class ReverseWhoisResponse:
  def __init__(self, response, target):
    self.target   = target
    self.response = response
    self._dict    = response.json()

  def render(self, CAP):
    _dict  = self._dict
    amount = _dict['domainsCount']
    output = ''

    if 'nextPageSearchAfter' in _dict.keys():
      next_page_search_after = _dict['nextPageSearchAfter']

    if amount > 0:
      output               += f'WhoisXMLApi found {str(amount)} domain results'

      if 'domainsList' in _dict.keys():
        output             += ':\n\n'
        i                   = 0

        for entry in _dict['domainsList']:
          i                   = i+1
          output             += f'  * {entry}\n'

          if CAP is not None and i == int(CAP):
            output           += f'\n Skipped output of {amount - i} other entries.\n'
            break
      else:
        output             += '.'

    else:
      output               += f'WhoisXMLApi found no domain results for {self.target}.'
    if 'nextPageSearchAfter' in _dict.keys() and next_page_search_after is not None:
      output               += f'Next search after: {next_page_search_after}'

    print(output)
