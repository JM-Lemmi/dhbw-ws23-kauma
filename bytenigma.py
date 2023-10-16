import base64

def bytenigma(data) -> None:
    """Run the bytenigma action."""

    rotors = data["rotors"]
    input = base64.b64decode(data["input"])

    print(encrypt_one(input[0], rotors))


def encrypt_one(input: bytes, rotors: list[list[int]]) -> bytes:
    # mit einem byte
    print("input: " + str(input))

    # schritt 1
    step_1_out = rotors[1][input]
    print("step 1: " + str(step_1_out))

    # schritt 2
    step_2_out = rotors[2][step_1_out]
    print("step 2: " + str(step_2_out))

    # bitweise komplement
    step_3_out = step_2_out^0xFF
    print("step 3: " + str(step_3_out))

    # schritt 4 (rotor 2 rückwärts)
    step_4_out = rotors[2].index(step_3_out)
    print("step 4: " + str(step_4_out))

    # schritt 5 (rotor 1 rückwärts)
    step_5_out = rotors[2].index(step_4_out)
    print("step 5: " + str(step_5_out))

    return step_5_out
