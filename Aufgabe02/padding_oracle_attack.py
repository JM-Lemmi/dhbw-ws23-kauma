#! /bin/python3

import socket
import time

ciphertext = bytes.fromhex('6946290be6dfa586724a360dfcc7a4ee') # changed ee to 00 in the end
l = 256

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 1337))
    print("Connected to padding oracle server...")

    s.sendall(ciphertext)
    s.sendall(l.to_bytes(2, byteorder='little'))
    
    for i in range(0, l):
        q = (b'\x00' * 15) + int.to_bytes(i, byteorder='little')
        s.sendall(q)

    print(f"Sent all data to padding oracle server, waiting for answer of length {l}...")

    success = bytearray()
    while len(success) < l: success += s.recv(1)

    for i, s in enumerate(success):
        if s == 1:
            print(f"Byte {i} is correct")
            exit(0)
        elif s == 0:
            print(f"Byte {i} is wrong")
        else:
            print(f"Weird Bytes returned, wtf: {s}")
