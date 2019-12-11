from itertools import zip_longest

opcodes = [
    (0x0000, 0xFFFF, "halt"),
    (0x0001, 0xF0FF, "read"),
    (0x0002, 0xF0FF, "write"),
    (0x0003, 0xF0FF, "jumpi"),
    (0x1000, 0xF000, "loadn"),
    (0x2000, 0xF000, "load"),
    (0x2000, 0xF000, "store"),
    (0x4000, 0xF00F, "loadi"),
    (0x4001, 0xF00F, "storei"),
    (0x4002, 0xF00F, "popr"),
    (0x4001, 0xF00F, "pushr"),
    (0x5000, 0xF000, "addn"),
    (0x6000, 0xFFFF, "nop"),
    (0x6000, 0xF00F, "mov"),
    (0x6000, 0xF000, "add"),
    (0x7000, 0xF0F0, "neg"),
    (0x7000, 0xF000, "sub"),
    (0x8000, 0xF000, "mul"),
    (0x9000, 0xF000, "div"),
    (0xA000, 0xF000, "mod"),
    (0xB000, 0xFF00, "jump"),
    (0xB000, 0xF000, "call"),
    (0xC000, 0xF000, "jeqz"),
    (0xD000, 0xF000, "jnez"),
    (0xE000, 0xF000, "jgtz"),
    (0xF000, 0xF000, "jltz"),
    (0x0000, 0x0000, "data"),
]

opdict = {name: code for code, _, name in opcodes}

# aliases = {
#     "setn":"loadn",
#     "copy":"mov",
#     "jumpn":"jump",
#     "jeqzn":"jeqz",
#     "jnezn":"jnez",
#     "jgtzn":"jgtz",
#     "jltzn":"jltz",
#     "calln":"call",
#     "jump":"jumpi",
#     "jumpr":"jumpi",
#     "loadn":"load",
#     "storen":"store",
#     "load":"loadi",
#     "loadr":"loadi",
#     "store":"storei",
#     "storer":"storei"
# }

arguments = {
    "halt": "",
    "read": "r",
    "write": "r",
    "jumpi": "r",
    "loadn": "rs",
    "load": "ru",
    "store": "ru",
    "loadi": "rr",
    "storei": "rr",
    "popr": "rr",
    "pushr": "rr",
    "addn": "rs",
    "add": "rrr",
    "mov": "rr",
    "nop": "",
    "sub": "rrr",
    "neg": "rzr",
    "mul": "rrr",
    "div": "rrr",
    "mod": "rrr",
    "jump": "zu",
    "call": "ru",
    "jeqz": "ru",
    "jgtz": "ru",
    "jltz": "ru",
    "jnez": "ru",
    "data": "n"
}

def unsign8(i):
    return i & 0xFF
def sign8(i):
    return ((i & 0xFF) ^ 0x80) - 0x80
def unsign16(i):
    return i & 0xFFFF
def sign16(i):
    return ((i & 0xFFFF) ^ 0x8000) - 0x8000

VERSION = 1