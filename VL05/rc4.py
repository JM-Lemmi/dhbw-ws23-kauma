#! /bin/python3

import sys

key = bytes.fromhex(sys.argv[1])
keylen = len(key)
sbox = list(range(256))

def ksa():
    j=0
    for i in range(256):
        j = (j + sbox[i] + key[i % keylen]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]
    
def gen_byte(n):
    i=0
    j=0
    while True:
        i = (i+1) % 256
        j = (j+sbox[i]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]
        yield sbox[(sbox[i]+sbox[j]) % 256]

keystream = bytearray()
ksa()
i = 0
for b in gen_byte(1):
    keystream.append(b)

    i += 1
    if i == 32:
        break

print(keystream.hex())
