#!/usr/bin/env python3

from sessions.exceptions import SubmissionException, RenderException, UnreachableException

class UrlscanResponse:
  def __init__(self, response, target):
    self.target   = target
    self.response = response
    self._dict    = response.json()

  def render(self):
    try:
      output         = ""

      if 'message' in self._dict and 'result' in self._dict:
        output      += self._dict['message']
        output      += ": "
        output      += self._dict['result']
        output      += " ("
        output      += self._dict['url']
        output      += ")."

      elif 'message' in self._dict and 'description' in self._dict:
        output      += f"Status {self._dict['status']}: "
        output      += self._dict['message']
        output      += '\nDescription: '
        output      += self._dict['description']

      else:
        output      += self._dict
      
      print(output)

    except Exception as f:
      if self.response.status_code is None:
        raise UnreachableException(f'{f}: Response status code is None.')
      elif self.response.status_code != 200:
        raise SubmissionException(f'Response code {self.response.status_code}: {self.response.message} ({self.target}).')
      else:
        raise RenderException(f'Render exception: {f}.\nResponse was:', str(self._dict))

