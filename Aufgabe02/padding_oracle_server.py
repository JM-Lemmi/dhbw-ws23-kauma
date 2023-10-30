#! /bin/python3

# usage: ./padding_oracle_server.py <listenport>

import socket
import sys

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', int(sys.argv[1]))) #v4-only :(
    s.listen()
    print("Server is listening...")

    # accept incoming connections
    client_socket, client_address = s.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    client_socket.sendall(b"Welcome to the padding oracle server!\n")

    s.close() #ich dachte das with kann das automatisch schließen, und es scheint auch nicht mehr so richt zu existieren, aber der port ist noch ghost belegt
