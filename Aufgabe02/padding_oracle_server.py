#! /bin/python3

# usage: ./padding_oracle_server.py <listenport>

import socket
import sys
import time

from cryptography.hazmat.primitives import padding

def xor(x, y): return bytes([a ^ b for a, b in zip(x, y)])

key = b'\x01\x23\x45\x67\x89\xab\xcd\xef\x01\x23\x45\x67\x89\xab\xcd\xef'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while True:
        try: s.bind(('127.0.0.1', int(sys.argv[1]))) #v4-only dank AF_INET. use AF_INET6 for v6
        except OSError: print("Port already in use, retrying..."); time.sleep(1)
        else: break

    s.listen()
    print("Server is listening...")

    try:
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
                print(l_int)

                a = bytearray() #results
                for i in range(l_int):
                    q = bytearray()
                    while len(q) < 16: q += client_socket.recv(1) # q
                    dc = xor(ciphertext, key)
                    plain = xor(dc, q)

                    try:
                        unpadder = padding.PKCS7(128).unpadder()
                        unpadder.update(plain)
                    except:
                        # unpadding failed
                        a += b'\x00'
                    else:
                        # unpadding succeeded
                        a += b'\x01'
                
                print(f"unpadding finished, sending results of length {len(a)}...")
                client_socket.sendall(a)

    except KeyboardInterrupt:
        print("\nExiting...")
        exit(0)
