#! /bin/python3

import socket
import time

def xor(x: bytes, y: bytes) -> bytes: return bytes([a ^ b for a, b in zip(x, y)])
def padleft(b: bytes, l: int) -> bytes: return (b'\x00' * (l - len(b))) + b
def padright(b: bytes, l: int) -> bytes: return b + (b'\x00' * (l - len(b)))

def pkcs7zeropad(l: int) -> bytes:
    """ Returns a valid pkcs7 padding of length l """
    if l > 16: raise ValueError("l must be <= 16")
    return (b'\x00' * (16 - l)) + int.to_bytes(l, byteorder='little') * l

ciphertext = bytes.fromhex('f680eaea09cfb737acd7bdde528bf05d')
iv = b'\x98\x91\xc0\xde\xe5\x92\x34\x15\xcc\x9f\xd8\xe6\xaf\xb2\x57\xe6'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 1337))
    print("Connected to padding oracle server...")

    s.sendall(ciphertext)

    dc = bytearray(b'\x00' * 16)
    for p in range(16): # länge des ciphers
        s.sendall(b'\x00\x01') # 256 q blocks (0x0100 in little endian)

        for i in range(256):
            q_short = padleft(int.to_bytes(i), 16-p) # counting 1-256, filled from the left with 0
            dc_p = xor(pkcs7zeropad(p+1), dc)[16-p:] # only the right bytes of dc with the correct padding xor.
            q = q_short + dc_p
            assert len(q) == 16
            s.sendall(q)

        print(f"Sent all data to padding oracle server, waiting for answer...")

        success = bytearray()
        while len(success) < 256: success += s.recv(1)

        for i, t in enumerate(success):
            if t == 1:
                # TODO: no check if the padding is correct on accident. one to the left of this position also needs to be roated as a test
                print(f"Byte {int.to_bytes(i, byteorder='little')} at position {p} is correct (before xor with padding)")
                dc[16-1-p] = xor(padleft(int.to_bytes(i, byteorder='big'), 16-p), pkcs7zeropad(p+1))[16-1-p] # set the correct byte in the zeroiv
            elif t == 0:
                #print(f"Byte {i} is wrong")
                pass
            else:
                print(f"Weird Bytes returned, wtf: {t}")
                exit(1)

    s.sendall(b'\x00\x00') # disconnect

    print(f"DC: {dc}")
    plain = xor(dc, iv)
    print(f"Plaintext is: {plain}")
