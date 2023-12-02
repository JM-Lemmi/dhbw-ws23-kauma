#! /bin/python3

import sys, os
import json
import base64

from Aufgabe01 import bytenigma
from Aufgabe02 import padding_oracle_attack
from Aufgabe03.galois_field import galois_field_element
from Aufgabe03 import gcm

import logging
if os.environ.get('DEBUG', False): logging.basicConfig(level=logging.DEBUG)

with open(sys.argv[1], 'r') as f:
  data = json.load(f)

match data["action"]:
  
  case 'bytenigma':
    output = bytenigma.bytenigma(data)
    json_out = json.dumps({"output": base64.b64encode(output).decode('utf-8')})
  
  case 'padding-oracle-attack':
    plaintext = padding_oracle_attack.attack(data["hostname"], data["port"], base64.b64decode(data["ciphertext"]), base64.b64decode(data["iv"]))
    json_out = json.dumps({"plaintext": base64.b64encode(plaintext).decode('utf-8')})
  
  case 'gcm-block2poly':
    exponents = galois_field_element.from_block(data["block"]).to_exponents()
    json_out = json.dumps({"exponents": exponents})
  
  case 'gcm-poly2block':
    block = galois_field_element.from_exponents(data["exponents"]).to_block()
    json_out = json.dumps({"block": block})
  
  case 'gcm-clmul':
    a = galois_field_element.from_block(data["a"])
    b = galois_field_element.from_block(data["b"])
    c = a*b
    json_out = json.dumps({"a_times_b": c.to_block()})
  
  case 'gcm-encrypt':
    ciphertext, auth_tag, Y0, H = gcm.gcm_encrypt(
      base64.b64decode(data["key"]),
      base64.b64decode(data["nonce"]),
      base64.b64decode(data["plaintext"]),
      base64.b64decode(data["associated_data"])
    )
    json_out = json.dumps(
      {"ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
       "auth_tag": base64.b64encode(auth_tag).decode('utf-8'),
       "Y0": base64.b64encode(Y0).decode('utf-8'),
       "H": base64.b64encode(H).decode('utf-8')}
    )
  
  case _:
    exit("Not implemented")

print(json_out)
