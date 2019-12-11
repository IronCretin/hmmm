#!/usr/bin/python
# hmmmSimulator.py
#
# $Id: hmmmSimulator.py,v 1.4 2007/10/08 08:10:12 geoff Exp $
#
# Ran Libeskind-Hadas, 2006
# modified by Peter Mawhorter, June 2006
# extensively modified by Geoff Kuenning, October 2007
# Swami Iyer (UMass Boston), 2015
#   - Modified read opcode to read without prompt and to read an integer 
#     from STDIN using the standard libraries from Princeton. This allows 
#     redirection of standard input using the < operator.
# Rewrittern by Paul Maynard, 2019


import sys
from hmmm import *
from array import array

def run(code):
    regs = array('h', [0] * 15)
    def putr(i, x):
        if i != 0: regs[i-1] = sign16(x)
    def getr(i):
        if i != 0: return regs[i-1]
        else: return 0
    mem = array('H')
    mem.extend(code)
    mem.extend([0] * (256 - len(code)))
    pc = 0
    while True:
        # print(pc)
        # print(regs)
        # print(mem)
        instr = mem[pc]
        # print(bin(instr))
        for opcode, mask, op in opcodes:
            if instr & mask == opcode:
                break
        if op == "halt":
            break
        elif op == "nop":
            pc += 1
        elif op == "read":
            r, = unpack(instr, arguments[op])
            putr(r, int(input()))
            pc += 1
        elif op == "write":
            r, = unpack(instr, arguments[op])
            print(getr(r))
            pc += 1
        elif op == "jumpi":
            i, = unpack(instr, arguments[op])
            pc = i
        elif op == "loadn":
            r, n = unpack(instr, arguments[op])
            putr(r, n)
            pc += 1
        elif op == "load":
            rdest, addr = unpack(instr, arguments[op])
            x = mem[addr]
            putr(rdest, x)
            pc += 1
        elif op == "store":
            rsrc, addr = unpack(instr, arguments[op])
            x = getr(rsrc)
            mem[addr] = unsign16(x)
            pc += 1
        elif op == "loadi":
            rdest, raddr = unpack(instr, arguments[op])
            x = mem[getr(raddr)]
            putr(rdest, x)
            pc += 1
        elif op == "storei":
            rsrc, raddr = unpack(instr, arguments[op])
            x = getr(rsrc)
            mem[getr(raddr)] = unsign16(x)
            pc += 1
        elif op == "addn":
            r, n = unpack(instr, arguments[op])
            putr(r, getr(r) + n)
            pc += 1
        elif op == "nop":
            pc += 1
        elif op == "mov":
            rdest, rsrc = unpack(instr, arguments[op])
            putr(rdest, getr(rsrc))
            pc += 1
        elif op == "add":
            rdest, rx, ry = unpack(instr, arguments[op])
            putr(rdest, getr(rx) + getr(ry))
            pc += 1
        elif op == "neg":
            rdest, rx = unpack(instr, arguments[op])
            putr(rdest, -getr(rx))
            pc += 1
        elif op == "sub":
            rdest, rx, ry = unpack(instr, arguments[op])
            putr(rdest, getr(rx) - getr(ry))
            pc += 1
        elif op == "mul":
            rdest, rx, ry = unpack(instr, arguments[op])
            putr(rdest, getr(rx) * getr(ry))
            pc += 1
        elif op == "div":
            rdest, rx, ry = unpack(instr, arguments[op])
            putr(rdest, getr(rx) / getr(ry))
            pc += 1
        elif op == "mod":
            rdest, rx, ry = unpack(instr, arguments[op])
            putr(rdest, getr(rx) % getr(ry))
            pc += 1
        elif op == "jump":
            i, = unpack(instr, arguments[op])
            pc = i
        elif op == "call":
            r, i = unpack(instr, arguments[op])
            putr(r, pc)
            pc = i
        elif op == "jeqz":
            r, i = unpack(instr, arguments[op])
            if getr(r) == 0:
                pc = i
            else:
                pc += 1
        elif op == "jgtz":
            r, i = unpack(instr, arguments[op])
            if getr(r) > 0:
                pc = i
            else:
                pc += 1
        elif op == "jltz":
            r, i = unpack(instr, arguments[op])
            if getr(r) < 0:
                pc = i
            else:
                pc += 1
        elif op == "jnez":
            r, i = unpack(instr, arguments[op])
            if getr(r) != 0:
                pc = i
            else:
                pc += 1
        elif op == "data":
            break

def unpack(instr, fields):
    offs = 12
    for f in fields:
        if f == 'z':
            offs -= 4
            continue
        elif f == 'r':
            offs -= 4
            yield (instr >> offs) & 0xF
        elif f == 'u':
            offs -= 8
            yield unsign8(instr >> offs)
        elif f == 's':
            offs -= 8
            yield sign8((instr >> offs) & 0xFF)
        elif f == 'n':
            yield sign16(i)

if __name__ == '__main__':
    with open(sys.argv[1] + '.b', 'rb') as f:
        length = int.from_bytes(f.read(2), sys.byteorder)
        code = array('H')
        code.fromfile(f, length)
        run(code)
