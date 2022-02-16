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

verify    = subparsers.add_parser('check', aliases=['-C'])
query     = subparsers.add_parser('query', aliases=['-Q'])
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
  nargs=2,
  required=False
)

query.add_argument(
  '--urlscan',
  default=SUPPRESS,
  help='Query Urlscan',
  nargs='*',
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

# VERIFY PARSER
verify.add_argument(
  '--email',
  default=SUPPRESS,
  help='Emailrep.io querying of an email address',
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
