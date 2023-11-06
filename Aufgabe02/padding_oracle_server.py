#! /bin/python3

# usage: ./padding_oracle_server.py <listenport>

import socket
import sys
from cryptography.hazmat.primitives import padding

def xor(x, y): return bytes([a ^ b for a, b in zip(x, y)])

key = b'0123456789abcdef'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', int(sys.argv[1]))) #v4-only dank AF_INET. use AF_INET6 for v6
    s.listen()
    print("Server is listening...")

    while True:
        # accept incoming connections
        client_socket, client_address = s.accept()
        with client_socket:
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

            #client_socket.sendall(b"Welcome to the padding oracle server!\n")

            ciphertext = bytearray()
            l = bytearray()
            while len(ciphertext) < 16: ciphertext += client_socket.recv(1) # Ciphertext
            while len(l) < 2: l += client_socket.recv(1) # l
            l_int = int.from_bytes(l, byteorder='little')

            qs = [bytearray()] * l_int
            for i in range(0, l_int):
                while len(qs[i]) < 16 * l_int: qs[i] += client_socket.recv(1) # q-blöcke
            
            print(f"Received all data from {client_address[0]}:{client_address[1]}, unpadding now...")

            for q in qs:
                dc = xor(ciphertext, key)
                xor(dc, q)

                try:
                    unpadder = padding.PKCS7(128).unpadder()
                    unpadder.update(dc)
                except:
                    client_socket.sendall(b'00')
                else:
                    client_socket.sendall(b'01')
