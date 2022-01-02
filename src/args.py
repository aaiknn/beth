#!/usr/bin/env python3

from argparse import ArgumentParser
from argparse import SUPPRESS

parser      = ArgumentParser()

subparsers  = parser.add_subparsers(
  title='modules',
  description='Beth verbs',
  help='Research steps'
)

peek      = subparsers.add_parser('lookup', aliases=['-L'])
stalk     = subparsers.add_parser('investigate', aliases=['-I'])

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

# STALK PARSER
stalk.add_argument(
  '--scan',
  default=SUPPRESS,
  help='Urlscan.io querying of a target',
  nargs=1,
  required=False
)

# EXPORT ARGS
def parse():
  args = parser.parse_args()
  return vars(args)
