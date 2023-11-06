#! /bin/python3

import socket
import time

def xor(x: bytes, y: bytes) -> bytes: return bytes([a ^ b for a, b in zip(x, y)])
def padleft(b: bytes, l: int) -> bytes: return (b'\x00' * (l - len(b))) + b

ciphertext = bytes.fromhex('6946290be6dfa586724a360dfcc7a4ee') # changed ee to 00 in the end

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 1337))
    print("Connected to padding oracle server...")

    s.sendall(ciphertext)

    key = bytearray(b'\x00' * 16)
    paddingrotator = bytearray(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08')
    for p in range(16): #länge des ciphers
        s.sendall(b'\x00\x01') # 256 q blocks
        
        for i in range(256):
            q = padleft(int.to_bytes(i, byteorder='little') * (256 ^ p), 16)
            q = xor(q, key)
            q = xor(q, padleft(paddingrotator[:p+1], 16))
            s.sendall(q)
            print(f"sent block {i}")

        print(f"Sent all data to padding oracle server, waiting for answer...")

        success = bytearray()
        while len(success) < 256: success += s.recv(1)

        for i, t in enumerate(success):
            if t == 1:
                print(f"Byte {i} at position {p} is correct")
                key[15-p] = i
            elif t == 0:
                print(f"Byte {i} is wrong")
            else:
                print(f"Weird Bytes returned, wtf: {t}")
    
    s.sendall(b'\x00\x00') # disconnect
    
    print(f"Key: {key.hex()}")
