
import logging
from typing import List

def block2poly(block: str) -> List[int]:
    l = []
    for i, v in enumerate(bin(int(block).hex(), base=16))[2:]: #decodes b64, then converts hex to int then to binary. [2:] removes the 0b prefix 
        if v == '1':
            l.append(i+2) # +2 because index starts at 2
        else:
            pass
