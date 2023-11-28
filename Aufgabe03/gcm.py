from __future__ import annotations
from typing import List

import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

from .galois_field import galois_field_element
def xor(x: bytes, y: bytes) -> bytes: return bytes([a ^ b for a, b in zip(x, y)]) # cannot import from Aufgabe02 because of python package bullshit

def aes_encrypt(key: bytes, plaintext: bytes) -> bytes:
    encryptor = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext

def ghash(H: bytes, A: bytes, C: List[str]) -> galois_field_element:
    """
    @returns: ghash value
    """

    H_gf = galois_field_element.from_blockbytes(H)
    A_gf = galois_field_element.from_blockbytes(A)
    step = A_gf * H_gf

    for i in range(len(C)):
        step = galois_field_element.from_blockbytes(C[i]) ^ step
        step = step * H_gf

    A_len = int.to_bytes(len(A)*8, 8, 'big') #8 because 8+8=16 und wir wollen 16 bytes
    C_len = int.to_bytes(len(C)*len(C[0])*8, 8, 'big')
    L = A_len + C_len # thats concatenation with bytes in python!

    step = step ^ galois_field_element.from_blockbytes(L)
    step = step * H_gf
    return step

def gcm_encrypt(key: bytes, nonce: bytes, plaintext: bytes, associated_data: bytes = None) -> (bytes, bytes, bytes, bytes):
    """
    @returns: (ciphertext, auth_tag, Y0, H)
    """

    ctr = 1
    Y0 = nonce + ctr.to_bytes(4, 'big')
    ctr += 1
    Y0encrypt = aes_encrypt(key, Y0)

    H = aes_encrypt(key, b'\x00'*16)

    ciphertexts = []
    for i in range(len(plaintext)//16):
        Y = nonce + ctr.to_bytes(4, 'big')
        ctr += 1
        AESout = aes_encrypt(key, Y)
        p = plaintext[i*16:(i+1)*16]
        if len(p) < 16: p += b'\x00'*(16-len(p)) # pad plaintext at the end
        ciphertexts.append(xor(p, AESout))
    
    gh = ghash(H, associated_data, ciphertexts)
    auth_tag = gh ^ galois_field_element.from_blockbytes(Y0encrypt)

    ciphertext = b''.join(ciphertexts)
    return (ciphertext, auth_tag.to_blockbytes(), Y0, H)
