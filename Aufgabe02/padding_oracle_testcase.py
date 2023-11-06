#! /bin/python3

from cryptography.hazmat.primitives import padding

#from padding_oracle_server import xor
def xor(x, y): return bytes([a ^ b for a, b in zip(x, y)])

key = b'\x01\x23\x45\x67\x89\xab\xcd\xef\x01\x23\x45\x67\x89\xab\xcd\xef'
plaintext = b'hellothisisjuli' + b'\x01' # valid pkcs7 padding

ciphertext = xor(plaintext, key)
print(ciphertext.hex())
print(len(ciphertext))
# 6946290be6dfa586724a360dfcc7a4ee

# decryption test
dc = xor(ciphertext, key)


for i in range(256):
    q = (b'\x00' * 15) + int.to_bytes(i, byteorder='little')
    print(q.hex())

    plain = xor(dc, q)

    print(f"Plain: {plain}")

# unpadding test

unpadder = padding.PKCS7(128).unpadder()
unpadder.update(plaintext)
unpadded = unpadder.finalize()

print(f"Unpadded: {unpadded}")

#this should crash
unpadder = padding.PKCS7(128).unpadder()
unpadder.update(b'hellothisisjuli' + b'\x02') # invalid pkcs7 padding
unpadded = unpadder.finalize()
