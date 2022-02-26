#!/usr/bin/env python3

class UsRecord:
  def __init__(self, api, country, message, options, result, url, uuid, visibility):
    self.api            = api
    self.country        = country
    self.message        = message
    self.options        = options
    self.result         = result
    self.url            = url
    self.uuid           = uuid
    self.visibility     = visibility

class UsMessage:
  def __init__(self, target, sc, message):
    self.message        = message
    self.result         = str(sc)
    self.url            = target

class UsResponse:
  def __init__(self, response):

    try:
      uuid = response['uuid']
      self.entry  = UsRecord(
        response['api'],
        response['country'],
        response['message'],
        response['options'],
        response['result'],
        response['url'],
        response['uuid'],
        response['visibility']
      )
    except Exception as f:
      raise f
