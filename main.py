#! /bin/python3

import sys
import json

with open(sys.argv[1], 'r') as f:
  data = json.load(f)

match data["action"]:
    case _:
        exit("Not implemented")
