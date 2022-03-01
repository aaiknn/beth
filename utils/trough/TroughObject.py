#!/usr/bin/env python3

# *- TroughObject
#  |
#  *- DomainTroughObject
#  *- UrlscanResultTroughObject
#  | |
#  | *- UrlscanQueryResultTroughObject
#  | *- UrlscanSubmissionResultTroughObject
#  |
#  *- WhoisXmlApiResultTroughObject

class TroughObject():
  def __init__(self, identifier, data):
    self.identifier = identifier
    self.data       = data

class DomainTroughObject(TroughObject):
  def __init__(self, identifier, data):
    self.whois            = ''
    self.dnsRecords       = ''

    super().__init__(identifier, data)

class UrlscanResultTroughObject(TroughObject):
  def __init__(self, urlscanResult):
    _dict       = urlscanResult
    identifier  = _dict['_id']

    super().__init__(identifier, _dict)

class UrlscanQueryResultTroughObject(UrlscanResultTroughObject):
  def __init__(self, urlscanResult):
    _dict = urlscanResult

    self.pageDomain       = _dict['page']['domain']
    self.pageUrl          = _dict['page']['url']
    self.pageAsn          = _dict['page']['asn']
    self.pageAsname       = _dict['page']['asnname']
    self.pageIP           = _dict['page']['ip']
    self.pageMimeType     = _dict['page']['mimeType']

    self.stats            = _dict['stats']
    self.statsRequests    = _dict['stats']['requests']

    self.bureaucracy      = _dict['sort']
    self.dateIndexed      = _dict['indexedAt']
    self.dateQueried      = _dict['task']['time']
    self.queryMethod      = _dict['task']['method']
    self.responseLocation = _dict['result']
    self.screenshot       = _dict['screenshot']

    super().__init__(_dict)

class WhoisXmlApiResultTroughObject(TroughObject):
  def __init__(self, whoisResult):
    _dict = whoisResult

    identifier = _dict[0]['domainName']

    super().__init__(identifier, _dict)
