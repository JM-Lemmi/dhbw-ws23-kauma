#! /bin/python3

from typing import List
from cryptography.hazmat.primitives import padding
import os

import padding_oracle_attack

server = "141.72.5.194"
port = 18732

def multiattack(server: str, port: int, iv: str, ciphertexts: List[str]) -> str:
    """ Attacks the server with multiple CBC ciphertexts and returns the unpadded plaintext"""
    q = bytes.fromhex(iv)
    plaintext = bytearray()

    for c in ciphertexts:
        ciphertext = bytes.fromhex(c)
        plaintext += padding_oracle_attack.attack(server, port, ciphertext, q)
        q = ciphertext
    
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(plaintext) + unpadder.finalize()

    return plaintext.decode('utf-8')

# Plantexte der 3 Aufgabeteile
plain23a = multiattack(server, port, "0478eabe443992c0b2b53cfc50aea04a", ["566b0c7206dbb19efa9b296696af2652", "d6900e8af1c80b3c79a3888f26bc3f18", "7153ee46bef72e70ec07c5d0ccde2c4f", "724bfe8c2e82458bf0c329f0a1393770", "50d21f2a3a7859d34cdb516750c4d1db", "9ce58f9872d87a31f6b0ba2f2ad5954f", "8334bb512ae7507b52e501b2e86ced6b"])
plain23b = multiattack(server, port, "4fd219786fc926b14ac605b939196546", ["3783a3acdea669ebc2a25faac92de5d2", "4f1b61d80c1110007855dbdb447278e6", "00a15dedf2291da7a7ac98e90ded950e", "23b81e6d9ddce5399b733956fd83986d", "21821fe00f4833eef95a7ab323e8bece", "a920642291948c6bc5c14511bf3dda1f", "a4f53424254f4e33a7097539b92d8612", "110aa72629e43ed763ab866dfaade621", "5cd895adc6a703bd2dc1627d7c51f0f2", "6240633bf1cf5f8ba0d136f6f66e4163", "8879081e1f4879810ae83ab01890de03", "6de960ffce2e89731d576044817dfef3", "64827a5485b0778492e7f524e42860aa"])
plain23c = multiattack(server, port, "6335b5933b0fe17eb023457e1dbb6244", ["8cc405bb829297f8e98e113dea8792f5", "3e416f023a38da02cfebabac13e2669a", "aa2248b3890eb356532e64c39d2c4938", "b5a425ce4809f0476f47b30d0e9fdf9a", "c8dc6af091cc534f5ea0049d3ebd63db"])

with open(os.path.abspath(os.path.dirname(__file__))+"/Aufgabe23.md", "w") as f:
    f.write(f"""# Aufgabe 2.3
## a)

{plain23a}

## b)

{plain23b}

## c)

{plain23c}
"""
    )
