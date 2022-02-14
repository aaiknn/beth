#!/usr/bin/env python3

from requests import get

from sessions.exceptions import EmailVerificationException, UnreachableException
from phrases import exceptions as e

email_check_url = 'https://emailrep.io/'

def verify_email(address):
  url       = email_check_url + address

  try:
    response  = get(url)
  except Exception as f:
    raise UnreachableException(f'{e.verify_email_failed}: {f}')

  if response.status_code == 200:
    result  = response.text
  elif response.status_code == 429:
    raise EmailVerificationException(f'{e.verify_email_failed}: Emailrep.io rate limit reached.')
  else:
    raise EmailVerificationException(f'{e.verify_email_failed}: Status not OK, but {response.status_code}.')

  return result

def verify(target):
  try:
    result = verify_email(target)
    print(result)
  except Exception as f:
    print(f'{e.verify_email_failed}: {f}')
