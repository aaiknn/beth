#!/usr/bin/env python3

from sessions.exceptions import SubmissionException

class UrlscanResponse:
  def __init__(self, response, target):
    self.target   = target
    self.response = response
    self._dict    = response.json()

  def render(self):
    try:
      output      = ""
      output      += self._dict['message']
      output      += ": "
      output      += self._dict['result']
      output      += " ("
      output      += self._dict['url']
      output      += ")."

      print(output)

    except Exception as f:
      if self.response.status_code is None:
        raise f

      elif self.response.status_code != 200:
        raise SubmissionException(f'Response code {self.response.status_code}: {self.response.message} ({self.target}).')

      else:
        print(str(self._dict))

