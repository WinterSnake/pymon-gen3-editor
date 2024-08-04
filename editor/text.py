#!/usr/bin/python
##-------------------------------##
## Pokemon Save Editor           ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Character Encoding            ##
##-------------------------------##

## Constants
__all__: tuple[str, str] = ("decode_string", "encode_string")
ENGLISH_CHARACTER_SET: dict[int, str] = {
    0xA1: '0',  0xA2: '1', 0xA3: '2', 0xA4: '3', 0xA5: '4', 0xA6: '5', 0xA7: '6', 0xA8: '7', 0xA9: '8', 0xAA: '9', 0xAB: '!',  0xAC: '?', 0xAD: '.',
    0xAE: '-',
    0xB4: '\'', 0xB5: '♂', 0xB6: '♀', 0xB8: ',', 0xBA: '/',
    0xBB: 'A',  0xBC: 'B', 0xBD: 'C', 0xBE: 'D', 0xBF: 'E', 0xC0: 'F', 0xC1: 'G', 0xC2: 'H', 0xC3: 'I', 0xC4: 'J', 0xC5: 'K', 0xC6: 'L', 0xC7: 'M',
    0xC8: 'N',  0xC9: 'O', 0xCA: 'P', 0xCB: 'Q', 0xCC: 'R', 0xCD: 'S', 0xCE: 'T', 0xCF: 'U', 0xD0: 'V', 0xD1: 'W', 0xD2: 'X', 0xD3: 'Y', 0xD4: 'Z',
    0xD5: 'a',  0xD6: 'b', 0xD7: 'c', 0xD8: 'd', 0xD9: 'e', 0xDA: 'f', 0xDB: 'g', 0xDC: 'h', 0xDD: 'i', 0xDE: 'j', 0xDF: 'k', 0xE0: 'l', 0xE1: 'm',
    0xE2: 'n',  0xE3: 'o', 0xE4: 'p', 0xE5: 'q', 0xE6: 'r', 0xE7: 's', 0xE8: 't', 0xE9: 'u', 0xEA: 'v', 0xEB: 'w', 0xEC: 'x', 0xED: 'y', 0xEE: 'z',
}


## Functions
def decode_string(_str: bytes) -> str:
    """Decode a string from the Gen3 character table and return a python string"""
    value: str = ""
    for byte in _str:
        if byte == 0xFF:
            break
        value += ENGLISH_CHARACTER_SET[byte]
    return value


def encode_string(_str: str, length: int = 0) -> bytes:
    """Encode a python string to the Gen3 character table and return the bytes"""
    value: bytearray = bytearray()
    if not length:
        length = len(_str) + 1
    for i in range(length):
        # -Append null character
        if i >= len(_str):
            value.append(0xFF)
            continue
        char = _str[i]
        # -Append character set
        for key, val in ENGLISH_CHARACTER_SET.items():
            if val == char:
                value.append(key)
                break
        if len(value) != i + 1:
            raise IndexError(f"Unhandled character '{char}' in table.")
    return bytes(value)
