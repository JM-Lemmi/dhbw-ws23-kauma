import base64
import logging
import hashlib

class Rotor:
    def __init__(self, rotor: list[int], next_rotor):
        self.rotor = rotor
        self.offset = 0
        self.next_rotor = next_rotor
        
        # reverse_rotor erstellen. allocated sofort das array und jumpt dann beim schreiben rum
        self.reverse_rotor = [None]*len(rotor)
        for i in range(len(rotor)):
            self.reverse_rotor[rotor[i]] = i

    def rotate(self) -> None:
        if self.rotor[self.offset] == 0 and self.next_rotor is not None:
            self.next_rotor.rotate()
            logging.debug("Überlauf des Rotors getriggert!")
        self.offset += 1
        self.offset %= 256 #wenn 256 erreicht wird zurückgesetzt

    def encrypt(self, input: int) -> int:
        return self.rotor[(input+self.offset)%256]

    def reverse_encrypt(self, input: int) -> int:
        return (self.reverse_rotor[input]-self.offset)%256

def bytenigma(data) -> bytes:
    """Run the bytenigma action."""

    rotors = data["rotors"]
    input = base64.b64decode(data["input"])
    rotorarray = []

    previous_rotor = None
    j = 0
    for i in reversed(rotors): # der loop muss rückwärts sein, damit der next_rotor schon existiert, wenn der rotor erstellt wird.
        rotorarray.append(Rotor(i, previous_rotor))
        previous_rotor = rotorarray[j]
        j += 1
    rotorarray = list(reversed(rotorarray)) # muss reversed werden, da die rotoren in der liste in umgekehrter reihenfolge sind

    output = b''
    for input_byte in input:
        output = output + encrypt_byte(input_byte, rotorarray)
        rotorarray[0].rotate()

    print(base64.b64encode(output))
    return output

def encrypt_byte(input: bytes, rotors: list[Rotor]) -> list[bytes]:
    # mit einem byte
    logging.debug(input, end=">")

    # vorwärts encrypten mit allen rotoren
    for r in rotors:
        input = r.encrypt(input)
        logging.debug(input, end=">")

    # bitweise komplement
    input = input^0xFF

    # alle rückwärts
    for r in reversed(rotors):
        input = r.reverse_encrypt(input)
        logging.debug(input, end=">")

    logging.debug(input)
    return bytes([input])
