#!/usr/bin/env python3

from os import environ as env
from dotenv import load_dotenv
from requests import get

from sessions.exceptions import AuthorisationException
from phrases import exceptions as e

load_dotenv()

endpoint = 'https://api.shodan.io/shodan/host/'

SHODAN_USER = env.get('API_KEY_SHODAN')

def make_pretty(response):
  _dict = response.json()
  _keys = _dict.keys()

  if 'dma_code' in _keys:
    t_dma_code      = _dict['dma_code']

  t_last_update   = _dict['last_update']
  t_tags          = _dict['tags']

  t_latitude      = _dict['latitude']
  t_longitude     = _dict['longitude']

  if 'postal_code' in _keys:
    t_postal_code   = _dict['postal_code']

  t_region_code   = _dict['region_code']
  t_area_code     = _dict['area_code']
  t_city          = _dict['city']
  t_country_name  = _dict['country_name']
  t_country_code  = _dict['country_code']

  if 'country_code3' in _keys:
    t_country_code3 = _dict['country_code3']

  t_org           = _dict['org']
  t_asn           = _dict['asn']
  t_isp           = _dict['isp']

  t_ip            = _dict['ip']
  t_ip_str        = _dict['ip_str']
  t_hostnames     = _dict['hostnames']
  t_domains       = _dict['domains']

  t_os            = _dict['os']
  t_ports         = _dict['ports']
  t_data          = _dict['data']

  output          = ''

  output         += f'Last update : {t_last_update}\n\n'
  output         += f'Org : {t_org}\n'
  output         += f'ISP : {t_isp}\n'
  output         += f'ASN : {t_asn}\n'

  if len(t_ports) > 0:
    output       += f'\nPorts:\n'

    for port in t_ports:
      output     += f'  * {port}\n'

  if len(t_data) > 0:
    output       += f'\nData :\n'

    for entry in t_data:
      _e_keys     = entry.keys()

      e_hash      = entry['hash']

      if 'http' in _e_keys:
        e_http      = entry['http']

      if 'tags' in _e_keys:
        e_tags      = entry['tags']

      e_time      = entry['timestamp']

      e_org       = entry['org']
      e_isp       = entry['isp']
      e_asn       = entry['asn']

      e_location  = entry['location']
      e_l_city    = e_location['city']
      e_l_area    = e_location['area_code']
      e_l_reg     = e_location['region_code']
      e_l_country = e_location['country_name']
      e_l_ccode   = e_location['country_code']

      e_l_lat     = e_location['latitude']
      e_l_lon     = e_location['longitude']

      if 'cloud' in _e_keys:
        e_cloud   = entry['cloud']
        e_c_reg   = e_cloud['region']
        e_c_serv  = e_cloud['service']
        e_c_prov  = e_cloud['provider']

        output   += f'Cloud provider : {e_c_prov} ({e_c_serv})\n'
        output   += f'Region         : {e_c_reg}\n\n'

      output     += f'Location  :\n'
      output     += f'City      : {e_l_city}, '

      if e_l_area is not None:
        output   += f'{e_l_area}, '

      output     += f'{e_l_reg}.\n'

      output     += f'Country   : {e_l_country} ({e_l_ccode}).\n'
      output     += f'Latitude  : {e_l_lat}\n'
      output     += f'Longitude : {e_l_lon}\n'

      if len(entry['hostnames']) > 0:
        output   += f'\nHostnames :\n'

        for name in entry['hostnames']:
          output += f'  * {name}\n'

      e_port      = entry['port']
      e_transp    = entry['transport']
      e_data      = entry['data']

      output     += f'\n{e_port}/{e_transp}:\n'
      output     += f'```txt\n{e_data}\n```\n'

  print(output)

def retrieve(*args, **options):
  target = args[0]
  response = get(f'{endpoint}{str(target)}?key={SHODAN_USER}')

  return(response)

def query(*args, **options):
  if SHODAN_USER is None:
    raise AuthorisationException(f'{e.query_shodan_failed}: Shodan API key missing.')

  else:
    response  = retrieve(*args, **options)
    sc        = response.status_code

    if sc == 200:
      make_pretty(response)

    else:
      print(response.status_code, response.text)

    return None
