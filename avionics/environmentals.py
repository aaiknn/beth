#!/usr/bin/env python3

from datetime import datetime
from logging import basicConfig, info, INFO

class EnvironmentalSenses():
  def __init__(self):
    basicConfig(
      format='%(asctime)s %(message)s',
      level=INFO,
      datefmt='%Y-%m-%d %H:%M:%S %z'
    )

  def info(self, message):
    info(message)

class SenseOfTime():

  def get_time(self, *args):
    timestamp = datetime.now()
    if len(args) > 0:
      timestamp = datetime.strftime(timestamp, *args)
    return timestamp

  def state_time(self, *args):
    timestamp = self.get_time(*args)
    print(timestamp)
