#! /bin/python3

import sys
import json
import base64

from Aufgabe01 import bytenigma
from Aufgabe02 import padding_oracle_attack

with open(sys.argv[1], 'r') as f:
  data = json.load(f)

match data["action"]:
  case 'bytenigma':
    output = bytenigma.bytenigma(data)
  case 'padding-oracle-attack':
    output = padding_oracle_attack.attack(data)
  case _:
    exit("Not implemented")

print(json.dumps({"output": base64.b64encode(output).decode('utf-8')}))
