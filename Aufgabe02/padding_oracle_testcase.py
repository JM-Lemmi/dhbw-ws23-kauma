#! /bin/python3

from cryptography.hazmat.primitives import padding

#from padding_oracle_server import xor
def xor(x, y): return bytes([a ^ b for a, b in zip(x, y)])

key = b'\x06\x74\x46\x58\x83\x29\xeb\x4b\x13\x21\x16\x52\x88\x55\xce\xba'
iv = b'\x98\x91\xc0\xde\xe5\x92\x34\x15\xcc\x9f\xd8\xe6\xaf\xb2\x57\xe6'
plaintext = b'hellothisisjuli' + b'\x01' # valid pkcs7 padding

dc = xor(plaintext, iv)
ciphertext = xor(dc, key)
print(ciphertext.hex())
print(len(ciphertext))
# f680eaea09cfb737acd7bdde528bf05d

# decryption test
dc = xor(ciphertext, iv)
plaintext = xor(dc, key)


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
