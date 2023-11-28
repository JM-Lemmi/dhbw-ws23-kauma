
from __future__ import annotations
import logging
import base64
from typing import List

# das halt richtig hässlich, aber python kann halt keine bytes ¯\_(ツ)_/¯
# wenn ich C könnte würde ich das da machen
def bytes_to_binstring(b: bytes) -> str:
    return ''.join(f'{x:08b}' for x in b)

# das ist nicht allgemein, sondern für aes_gcm
class galois_field_element:

    ### CONSTRUCTORS and EXPORTERS ###

    def __init__(self, value: int = None):
        self.value: int = value

    @staticmethod
    def from_exponents(exponents: List[int]) -> galois_field_element:
        """ constructor: list of exponents as input """
        v=0
        for i in exponents:
            v = (2 ** i) + v
        return galois_field_element(v)

    @staticmethod
    def from_block(block: str) -> galois_field_element:
        """ constructor: base64 string block as input """
        l = []
        for i, v in enumerate(bytes_to_binstring(base64.b64decode(block))): # decode b64, then concert to binary string
            if v == '1':
                l.append(i)
            else:
                pass
        return galois_field_element.from_exponents(l)
    
    def to_exponents(self) -> List[int]:
        """ return list of exponents """
        l = []
        for i in range(self.value.bit_length()):
            if self.value & (1 << i):
                l.append(i)
        
        return sorted(l)

    """
    gets array of exponents and returns base64 encoded block
    """
    def to_block(self) -> str:
        exponents = self.to_exponents()

        block = [0] * 128
        for i in exponents:
            block[i] = '1'

        blockstr: str = ""
        for j in block:
            blockstr = blockstr + str(j)
        
        return str(base64.b64encode(int(blockstr, base=2).to_bytes(length=16, byteorder='big')), 'utf-8')

    ### OPERATORS ###
    
    def __mul__(self, other: galois_field_element) -> galois_field_element:
        result = 0

        for e in other.to_exponents():
            result = result ^ (self.value << e)

        gf = galois_field_element(result)
        gf._reduce()
        return gf
    
    def _reduce(self):
        r = galois_field_element.from_exponents([128,7,2,1,0])

        while self.value.bit_length() >= r.value.bit_length():
            rs: int = r.value << (self.value.bit_length() - r.value.bit_length())
            self.value = self.value ^ rs
