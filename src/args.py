#!/usr/bin/env python3

from argparse import ArgumentParser
from argparse import SUPPRESS
from sys import argv

parser      = ArgumentParser()

subparsers  = parser.add_subparsers(
  title='modules',
  description='Beth verbs',
  help='Research steps'
)

stare     = subparsers.add_parser('investigate', aliases=['-I'])
peek      = subparsers.add_parser('lookup', aliases=['-L'])
record    = subparsers.add_parser('record', aliases=['-S'])

# PEEK PARSER
peek.add_argument(
  '--dns',
  default=SUPPRESS,
  help='DNS lookup of a target',
  nargs=1,
  required=False
)

peek.add_argument(
  '--reverse',
  default=SUPPRESS,
  help='Reverse IP lookup of a target',
  nargs=1,
  required=False
)

# STARE PARSER
stare.add_argument(
  '--scan',
  default=SUPPRESS,
  help='Urlscan.io querying of a target',
  nargs=1,
  required=False
)

# EXPORT ARGS
def parse():
  args = [
    argv[1],
    parser.parse_args()
  ]
  return args
