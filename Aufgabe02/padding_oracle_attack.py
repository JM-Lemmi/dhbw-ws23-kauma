#! /bin/python3

import socket

ciphertext = bytes.fromhex('2d5cb7e89318651744664fbee709e147')
l = 3

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 1337))
    print("Connected to padding oracle server...")

    s.sendall(ciphertext)
    s.sendall(l.to_bytes(2, byteorder='little'))
    for i in range(0, l):
        s.sendall(b'00' * 15 + int.to_bytes(i, byteorder='little'))

    print("Sent all data to padding oracle server, waiting for answer...")

    for i in range(0, l):
        success = s.recv(2)
        if success == b'00':
            print(f"Byte {i} is correct")
        elif success == b'01':
            print(f"Byte {i} is wrong")
        else:
            print(f"Weird Bytes returned, wtf: {success}")
