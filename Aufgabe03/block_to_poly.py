
import logging
import base64
from typing import List

# das halt richtig hässlich, aber python kann halt keine bytes ¯\_(ツ)_/¯
# wenn ich C könnte würde ich das da machen
def bytes_to_binstring(b: bytes) -> str:
    return ''.join(f'{x:08b}' for x in b)

def block2poly(block: str) -> List[int]:
    l = []
    for i, v in enumerate(bytes_to_binstring(base64.b64decode(block))): # decode b64, then concert to binary string
        if v == '1':
            l.append(i) # +2 because index starts at 2
        else:
            pass
    return l

"""
gets array of exponents and returns base64 encoded block
"""
def poly2block(exponents: List[int]) -> str:
    block = [0] * 128
    for i in exponents:
        block[i] = '1'

    blockstr: str = ""
    for j in block:
        blockstr = blockstr + str(j)
    
    return str(base64.b64encode(int(blockstr, base=2).to_bytes(length=16, byteorder='big')), 'utf-8')
