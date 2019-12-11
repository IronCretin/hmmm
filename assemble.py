#!/usr/bin/python
#
# $Id: hmmmAssembler.py,v 1.4 2007/10/08 08:10:11 geoff Exp $
#
# hmmmAssembler.py
# Ran Libeskind-Hadas, 2006
# modified by Peter Mawhorter, June 2006
# Extensively modified by Geoff Kuenning, October 2007
# modified by Kaya Woodall, June 2012
# rewritten by Paul Maynard, December 2019

import re
from array import array
from hmmm import *
import sys

def parse(lines):
    for line in lines:
        line = line.partition('#')[0].strip()
        if line:
            line, instr, args = re.fullmatch(r'(\d+)\s+(\w+)(?:\s+([\w -]+)|)', line).groups()
            line = int(line)
            if args:
                args = re.split(r'\s+', args)
            else:
                args = []
            yield line, instr, args

def pack(name, args):
    # name = aliases.get(name, name)
    op = opdict[name]
    fields = arguments[name]
    i = 0
    offs = 12
    for f in fields:
        if f == 'z':
            offs -= 4
            continue
        elif f == 'r':
            offs -= 4
            arg = args[i]
            if arg[0] != 'r': raise ValueError
            arg = int(arg[1:])
            if not (0 <= arg <= 15): raise ValueError
            op |= (arg & 0xF) << offs
        elif f == 'u':
            offs -= 8
            arg = int(args[i], base=0)
            if not (0 <= arg <= 255): raise ValueError
            op |= (arg & 0xFF) << offs
        elif f == 's':
            offs -= 8
            arg = int(args[i], base=0)
            if not (-128 <= arg <= 127): raise ValueError
            op |= (arg & 0xFF) << offs
        elif f == 'n':
            arg = int(args[i], base=0)
            op = arg & 0xFFFF
        i += 1
    return op

def assemble(lines):
    out = array('H')
    for line, name, args in lines:
        if len(out) <= line:
            out.extend([0] + [0] * (line - len(out)))
        out[line] = pack(name, args)
    # if sys.byteorder == 'little': out.byteswap()
    return out

if __name__ == "__main__":
    with open(sys.argv[1] + '.hmmm') as fin, open(sys.argv[1] + '.b', 'wb') as fout:
        code = assemble(parse(fin))
        fout.write(len(code).to_bytes(2, sys.byteorder))
        code.tofile(fout)