#! /bin/python3

import matplotlib.pyplot
import numpy
import random
import base64
import os

import bytenigma

def generate_rotor() -> list[int]:
    numbers = list(range(256))
    # shuffle randomly
    random.shuffle(numbers)
    return numbers

with open("words_alpha.txt", "rb") as f:
    input = f.read()

# erstelle zufällige bytenigmarotoren
data = {}
data["rotors"] = [generate_rotor(), generate_rotor(), generate_rotor()]
data["input"] = base64.b64encode(input)
output = bytenigma.bytenigma(data)

charcount = [None]*255
for i in range(0, 255):
    charcount[i] = output.count(i)

#charcount = charcount[1:] # das erste element ist immer 0, da es keine 0en gibt. Für Plot2
matplotlib.pyplot.stem(charcount, bottom=numpy.average(charcount))
matplotlib.pyplot.show()

print(charcount)
