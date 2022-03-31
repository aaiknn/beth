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
test      = subparsers.add_parser('test', aliases=['-T'])
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

peek.add_argument(
  '--whois',
  default=SUPPRESS,
  help='Whois lookup of a target',
  nargs=1,
  required=False
)

peek.add_argument(
  '--rwhois',
  default=SUPPRESS,
  help='Reverse whois lookup of a target',
  nargs=1,
  required=False
)

peek.add_argument(
  '--after', '-A',
  default=SUPPRESS,
  help='Find records that have been created after a given date (format: YYYY-MM-DD).',
  type=str,
  dest='after',
  nargs=1,
  required=False
)

peek.add_argument(
  '--before', '-B',
  default=SUPPRESS,
  help='Find records that have been created before a given date (format: YYYY-MM-DD).',
  type=str,
  dest='before',
  nargs=1,
  required=False
)

peek.add_argument(
  '--between', '-X',
  default=SUPPRESS,
  help='Find records that have been created between two given dates (format: YYYY-MM-DD).',
  type=str,
  dest='between',
  nargs=2,
  required=False
)

peek.add_argument(
  '-H',
  default=SUPPRESS,
  help='Historic lookup (if available)',
  action='store_const',
  const='HISTORIC',
  dest='options',
  required=False
)

peek.add_argument(
  '-F',
  default=SUPPRESS,
  help='Runs lookup against bulk data in a specified file',
  action='store_const',
  const='BULK_FILE',
  dest='options',
  required=False
)

peek.add_argument(
  '--mode', '-M',
  default=SUPPRESS,
  help='Mode of reverse lookup ("default" or "preview")',
  type=str,
  nargs=1,
  required=False
)

query.add_argument(
  '--urlscan',
  default=SUPPRESS,
  help='Query Urlscan',
  nargs='*',
  required=False
)

query.add_argument(
  '-R',
  default=SUPPRESS,
  help='Set repeated Urlscan query switch',
  action='store_const',
  const='REPEAT',
  dest='options',
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

stare.add_argument(
  '--shodan',
  default=SUPPRESS,
  help='Shodan querying of a target',
  nargs=1,
  required=False
)

# TEST PARSER
test.add_argument(
  '--status',
  default=SUPPRESS,
  help='Test for URL HTTP response status',
  nargs=1,
  required=False
)

test.add_argument(
  '--up',
  default=SUPPRESS,
  help='Test for URL HTTP response',
  nargs=1,
  required=False
)

test.add_argument(
  '-F',
  default=SUPPRESS,
  help='Run tests against bulk data in a specified file',
  action='store_const',
  const='BULK_FILE',
  dest='options',
  required=False
)

test.add_argument(
  '-v',
  default=SUPPRESS,
  help='Prints more in-depth information on test results',
  action='store_const',
  const=1,
  dest='verbosity',
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
