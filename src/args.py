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

# PEEK PARSER
peek.add_argument(
  '--dns',
  default=SUPPRESS,
  help='DNS lookup of a target',
  nargs=1,
  required=False
)

# EXPORT ARGS
def parse():
  args = parser.parse_args()
  return vars(args)
