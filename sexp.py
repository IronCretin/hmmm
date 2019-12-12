from enum import Enum, auto
from collections import namedtuple
import re

class Tok(Enum):
    OPEN = auto()
    CLOSE = auto()
    NAME = auto()
    NUM = auto()
Token = namedtuple('Token', 'type val')

def tokenize(s):
    toks = re.findall(r"[()]|[^()\s]+(?=[\s()])", s)
    for t in toks:
        if t == '(':
            yield Token(Tok.OPEN, t)
        elif t == ')':
            yield Token(Tok.CLOSE, t)
        elif re.match(r'^\d', t):
            yield Token(Tok.NUM, int(t, base=0))
        else:
            yield Token(Tok.NAME, t)

def sexp(toks, level=0):
    toks = iter(toks)
    lis = []
    for typ, val in toks:
        if typ == Tok.OPEN:
            lis.append(sexp(toks, level+1))
        elif typ == Tok.CLOSE and level != 0:
            return lis
        elif typ == Tok.NAME:
            lis.append(val)
        elif typ == Tok.NUM:
            lis.append(val)
    if level == 0:
        return lis
    else:
        raise ValueError
