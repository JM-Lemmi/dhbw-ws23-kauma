#! /bin/python3

# usage: ./padding_oracle_server.py <listenport>

import socket
import sys
import cryptography

def xor(x, y): return bytes([a ^ b for a, b in zip(x, y)])

key = b'0123456789abcdef'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', int(sys.argv[1]))) #v4-only dank AF_INET. use AF_INET6 for v6
    s.listen()
    print("Server is listening...")

    while True:
        # accept incoming connections
        client_socket, client_address = s.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        client_socket.sendall(b"Welcome to the padding oracle server!\n")
        ciphertext = client_socket.recv(16) # Ciphertext
        l = client_socket.recv(2) # l
        l_int = int.from_bytes(l, byteorder='little')

        qs = [None] * l_int
        for i in range(0, l_int):
            qs[i] = client_socket.recv(16 * l) # q-blöcke

        for q in qs:
            dc = xor(ciphertext, key)
            xor(dc, q)

            # TODO: check padding here
            try:
                cryptography.unpadder(dc, 16)
            except:
                client_socket.sendall(b'00')
            else:
                client_socket.sendall(b'01')

        client_socket.close()

    s.close() #ich dachte das with kann das automatisch schließen, und es scheint auch nicht mehr so richt zu existieren, aber der port ist noch ghost belegt. netstat -tulpen zeigt ihn nicht mehr als belegt an, aber wenn ich den server neu starte, kommt die fehlermeldung, dass der port schon belegt ist. wenn ich den port ändere, gehts wieder.
        # needs reuse
