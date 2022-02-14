#!/usr/bin/env python3

from requests import get

from sessions.exceptions import EmailVerificationException

email_check_url = 'https://emailrep.io/'

def verify_email(address):
  url       = email_check_url + address
  response  = get(url)

  if response.status_code == 200:
    result  = response.text
  else:
    raise EmailVerificationException(f'Unable to verify email address: status not OK, but {response.status_code}.')

  return result

def verify(target):
  try:
    result = verify_email(target)
    print(result)
  except Exception as f:
    print(f)
