#! /bin/python3

import socket
import time

ciphertext = bytes.fromhex('6946290be6dfa586724a360dfcc7a4ee')
l = 256

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 1337))
    print("Connected to padding oracle server...")

    s.sendall(ciphertext)
    s.sendall(l.to_bytes(2, byteorder='little'))
    for i in range(0, l):
        s.sendall((b'\x00' * 15) + int.to_bytes(i, byteorder='little'))

    print("Sent all data to padding oracle server, waiting for answer...")

    for i in range(0, l):
        success = s.recv(1)
        if success == b'\x00':
            print(f"Byte {i} is correct")
            exit(0)
        elif success == b'\x01':
            print(f"Byte {i} is wrong")
        else:
            print(f"Weird Bytes returned, wtf: {success}")
