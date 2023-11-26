#! /bin/python3

import socket
import logging

def xor(x: bytes, y: bytes) -> bytes: return bytes([a ^ b for a, b in zip(x, y)])
def padleft(b: bytes, l: int) -> bytes: return (b'\x00' * (l - len(b))) + b
def padright(b: bytes, l: int) -> bytes: return b + (b'\x00' * (l - len(b)))

def pkcs7zeropad(l: int) -> bytes:
    """ Returns a valid pkcs7 padding of length l """
    if l > 16: raise ValueError("l must be <= 16")
    return (b'\x00' * (16 - l)) + int.to_bytes(l, length=1, byteorder='little') * l

def attack(hostname: str, port: int, ciphertext: bytes, iv: bytes) -> bytes:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((hostname, port))
        logging.debug("Connected to padding oracle server...")

        s.sendall(ciphertext)

        dc = bytearray(b'\x00' * 16)
        for p in range(16): # länge des ciphers
            s.sendall(b'\x00\x01') # 256 q blocks (0x0100 in little endian)

            for i in range(256):
                q_short = padleft(int.to_bytes(i, length=1, byteorder='big'), 16-p) # counting 1-256, filled from the left with 0
                dc_p = xor(pkcs7zeropad(p+1), dc)[16-p:] # only the right bytes of dc with the correct padding xor.
                q = q_short + dc_p
                assert len(q) == 16
                s.sendall(q)

            logging.debug(f"Sent all data to padding oracle server, waiting for answer...")

            success = bytearray()
            while len(success) < 256: success += s.recv(1)

            for i, t in enumerate(success):
                if t == 1:
                    if p == 15:
                        # correct, no false positive possible
                        logging.debug(f"Byte {int.to_bytes(i, length=1, byteorder='little')} at position {p} is correct (before xor with padding)")
                        dc[16-1-p] = xor(padleft(int.to_bytes(i, length=1, byteorder='big'), 16-p), pkcs7zeropad(p+1))[16-1-p] # set the correct byte in the zeroiv
                    else:
                        # Checking for false positive
                        # repeating code from ln 28ff.
                        q_short = padleft(b'\xff' + int.to_bytes(i, length=1, byteorder='big'), 16-p) # added 0xff (inverse of 0x00) left of the currently counting number
                        dc_p = xor(pkcs7zeropad(p+1), dc)[16-p:]
                        q = q_short + dc_p
                        assert len(q) == 16

                        s.sendall(b'\x01\x00')
                        s.sendall(q)
                        sucdouble = s.recv(1)
                        if sucdouble == b'\x01':
                            # true positive
                            logging.debug(f"Byte {int.to_bytes(i, length=1, byteorder='little')} at position {p} is correct (before xor with padding)")
                            dc[16-1-p] = xor(padleft(int.to_bytes(i, length=1, byteorder='big'), 16-p), pkcs7zeropad(p+1))[16-1-p] # set the correct byte in the zeroiv
                        else:
                            # false positive
                            logging.debug(f"Byte {int.to_bytes(i, length=1, byteorder='little')} at position {p} is wrong (false positive)")

                    
                elif t == 0:
                    #logging.debug(f"Byte {i} is wrong")
                    pass
                else:
                    logging.debug(f"Weird Bytes returned, wtf: {t}")
                    exit(1)

        s.sendall(b'\x00\x00') # disconnect

        logging.debug(f"DC: {dc}")
        plain = xor(dc, iv)
        logging.debug(f"Plaintext is: {plain}")
        return plain
