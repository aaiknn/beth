#!/usr/bin/env python3

from requests import get

from sessions.exceptions import EmailVerificationException, UnreachableException
from phrases import exceptions as e

email_check_url = 'https://emailrep.io/'

def colour_code(term, suspicion_status):
  if suspicion_status == True:
    return f'\033[31m{str(term)}\033[0m'
  else:
    return f'\033[33m{str(term)}\033[0m'

def make_pretty(response):
  _dict         = response.json()
  t_details     = _dict['details']

  target        = _dict['email']
  t_refs        = _dict['references']
  t_rep         = _dict['reputation']
  t_sus         = _dict['suspicious']
  t_tld_sus     = t_details['suspicious_tld']
  t_spoofable   = t_details['spoofable']
  t_valid_mx    = t_details['valid_mx']
  t_main_mx     = t_details['primary_mx']

  t_seen_first  = t_details['first_seen']
  t_seen_last   = t_details['last_seen']

  t_breached    = t_details['data_breach']
  t_creds_f     = t_details['credentials_leaked']
  t_creds_f_r   = t_details['credentials_leaked_recent']

  t_blocklisted = t_details['blacklisted']
  t_maltivity   = t_details['malicious_activity']
  t_maltivity_r = t_details['malicious_activity_recent']
  t_spam        = t_details['spam']

  t_d_exists    = t_details['domain_exists']
  t_d_rep       = t_details['domain_reputation']
  t_d_fresh     = t_details['new_domain']
  t_d_existtime = t_details['days_since_domain_creation']
  t_d_free      = t_details['free_provider']

  t_disposable  = t_details['disposable']
  t_deliverable = t_details['deliverable']
  t_accept_all  = t_details['accept_all']
  t_spf_strict  = t_details['spf_strict']
  t_dmarc       = t_details['dmarc_enforced']

  t_profiles    = t_details['profiles']
  c_rep         = colour_code(t_rep, t_sus)

  result        = ''
  result       += f'Address \033[1m{target}\033[0m reputation is {t_rep}.\n'
  result       += f'Suspicious : {str(t_sus)}\n'
  result       += f'\nVERDICT DETAILS :\n\n'
  result       += f'TLD suspicious   : {str(t_tld_sus)}\n'
  result       += f'Valid MX         : {str(t_valid_mx)}\n'
  result       += f'Primary MX       : {str(t_main_mx)}\n\n'
  result       += f'First seen       : {str(t_seen_first)}\n'
  result       += f'Last seen        : {str(t_seen_last)}\n\n'
  result       += f'Breached                     : {str(t_breached)}\n'
  result       += f'Credentials leaked           : {str(t_creds_f)}\n'
  result       += f'Credentials leaked recently  : {str(t_creds_f_r)}\n\n'
  result       += f'Blocklisted                  : {str(t_blocklisted)}\n'
  result       += f'Malicious activity           : {str(t_maltivity)}\n'
  result       += f'Recent malicious activity    : {str(t_maltivity_r)}\n'
  result       += f'Spam                         : {str(t_spam)}\n\n'
  result       += f'Domain exists       : {str(t_d_exists)}\n'
  result       += f'Domain age          : {str(t_d_existtime)}\n'
  result       += f'Domain young        : {str(t_d_fresh)}\n\n'
  result       += f'Free provider       : {str(t_d_free)}\n\n'
  result       += f'Disposable          : {str(t_disposable)}\n'
  result       += f'Deliverable         : {str(t_disposable)}\n'
  result       += f'Accept all          : {str(t_accept_all)}\n'
  result       += f'SPF strict          : {str(t_spf_strict)}\n'
  result       += f'DMARC enforced      : {str(t_disposable)}\n\n'
  result       += f'Profiles associated : {str(len(t_profiles))}'

  if len(t_profiles) > 0:
    result     += ' ('

    for entry in t_profiles:
      result   += entry
      result   += ' '

    result     += ')'

  print(result)

def verify_email(*args, **options):
  url       = email_check_url + args[0]
  try:
    response  = get(url)

  except Exception as f:
    raise UnreachableException(f'{e.verify_email_failed}: {f}')

  if response.status_code == 200:
    return response

  elif response.status_code == 429:
    raise EmailVerificationException(f'{e.verify_email_failed}: Emailrep.io rate limit reached.')

  else:
    raise EmailVerificationException(f'{e.verify_email_failed}: Status not OK, but {response.status_code}.')

def verify(trough, *args, **options):
  try:
    response = verify_email(*args, **options)
    make_pretty(response)

  except Exception as f:
    print(f'{e.verify_email_failed}: {f}')
