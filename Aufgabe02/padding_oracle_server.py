#! /bin/python3

# usage: ./padding_oracle_server.py <listenport>

import socket
import sys
import time

from cryptography.hazmat.primitives import padding

def xor(x, y): return bytes([a ^ b for a, b in zip(x, y)])

key = b'\x06\x74\x46\x58\x83\x29\xeb\x4b\x13\x21\x16\x52\x88\x55\xce\xba'

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

                ciphertext = bytearray()
                while len(ciphertext) < 16: ciphertext += client_socket.recv(1) # Ciphertext

                while True:
                    l = bytearray()
                    while len(l) < 2: l += client_socket.recv(1) # l
                    l_int = int.from_bytes(l, byteorder='little')
                    if l_int == 0: print("Received Disconnect from Client"); break #allows receiving multiple batches of q until 0x0000 is sent as l
                    print(f"Waiting to receive {l_int} blocks...")

                    a = bytearray() #results
                    for i in range(l_int):
                        q = bytearray()
                        while len(q) < 16: q += client_socket.recv(1) # q
                        dc = xor(ciphertext, key) # <- this is decryption
                        plain = xor(dc, q)        # <- this is cbc

                        try:
                            unpadder = padding.PKCS7(128).unpadder()
                            unpadder.update(plain)
                            unpadder.finalize()
                        except ValueError:
                            # unpadding failed
                            a += b'\x00'
                        else:
                            # unpadding succeeded
                            a += b'\x01'
                            print(f"Unpadding succeeded at position {i}.")
                    
                    print("Unpadding finished.")
                    client_socket.sendall(a)

    except KeyboardInterrupt:
        print("\nExiting...")
        s.close() #with catcht hier nicht, daher manuell schließen
        client_socket.close()
        exit(0)
