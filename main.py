#! /bin/python3

import sys
import json

import bytenigma

with open(sys.argv[1], 'r') as f:
  data = json.load(f)

match data["action"]:
  case 'bytenigma':
    bytenigma.bytenigma(data)
  case _:
    exit("Not implemented")
