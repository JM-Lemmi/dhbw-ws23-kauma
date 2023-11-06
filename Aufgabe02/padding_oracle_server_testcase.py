#! /bin/python3

#from padding_oracle_server import xor
def xor(x, y): return bytes([a ^ b for a, b in zip(x, y)])

key = b'\x01\x23\x45\x67\x89\xab\xcd\xef\x01\x23\x45\x67\x89\xab\xcd\xef'
plaintext = b'hellothisisjuli' + b'\x01'

ciphertext = xor(plaintext, key)
print(ciphertext.hex())
print(len(ciphertext))
# 6946290be6dfa586724a360dfcc7a4ee
