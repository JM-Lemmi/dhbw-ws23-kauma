#! /bin/python3

import sys
import json
import base64

import bytenigma

with open(sys.argv[1], 'r') as f:
  data = json.load(f)

match data["action"]:
  case 'bytenigma':
    output = bytenigma.bytenigma(data)
  case _:
    exit("Not implemented")

print(json.dumps({"output": base64.b64encode(output).decode('utf-8')}))
