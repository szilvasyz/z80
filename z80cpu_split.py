from utils import *
from z80regs import registers
from mod_prefix import prefix
from mod_load import load
from mod_inout import inout
from mod_stack import stack
from mod_alu import alu
from mod_jump import jump
from mod_incdec import incdec
from mod_bits import bits
from mod_block import block


#
# CPU main class
#


class cpu():

    def __init__(self):
        self.r = registers(self)
        self.mem = []
        self.inp = []
        self.out = []
        self.iff1 = 0
        self.iff2 = 0
        self.im = 0
        self.halted = False

        self.dsp = 0
        self.opc = b''
        self.r0 = 0
        self.r1 = 0
        self.rp = 0
        self.next = False

        self.instr = {}

        mods = [prefix(self), load(self), inout(self), stack(self),
                alu(self), jump(self), incdec(self), bits(self), block(self)]
        for mod in mods:
            self.instr.update(mod.getinstr())

    def __str__(self):
        return str(self.r)

    def addinp(self, inpobj):
        self.inp.append(inpobj)

    def rdinp(self, addr):
        for m in self.inp:
            if addr in m.keys():
                return m[addr]
        return 0xFF

    def addout(self, outobj):
        self.out.append(outobj)

    def wrout(self, addr, data):
        for m in self.out:
            if addr in m.keys():
                m[addr] = data
        return

    def addmem(self, memobj):
        self.mem.append(memobj)

    def rdmem(self, addr):
        for m in self.mem:
            if addr in m.keys():
                return m[addr]
        return 0xFF

    def wrmem(self, addr, data):
        for m in self.mem:
            if addr in m.keys():
                m[addr] = data
        return

    def rdmem16(self, addr):
        return self.rdmem(addr) | (self.rdmem(inc16(addr)) << 8)

    def wrmem16(self, addr, data):
        self.wrmem(addr, lobyte(data))
        self.wrmem(inc16(addr), hibyte(data))
        return

    def push(self, data):
        a = word(self.r["SP"] - 2)
        self.wrmem16(a, data)
        self.r["SP"] = a

    def pop(self):
        a = self.r["SP"]
        d = self.rdmem16(a)
        self.r["SP"] = word(a + 2)
        return d

    def fetch(self):
        d = self.rdmem(self.r["PC"])
        self.r["PC"] = inc16(self.r["PC"])
        return d

    def fetch16(self):
        d = self.rdmem(self.r["PC"])
        self.r["PC"] = inc16(self.r["PC"])
        d = d | (self.rdmem(self.r["PC"]) << 8)
        self.r["PC"] = inc16(self.r["PC"])
        return d

    def step(self):
        self.next = True
        self.opc = b''
        while self.next:
            s = ''
            self.next = False
            b = self.fetch()
            self.r0 = (b >> 3) & 7
            self.r1 = b & 7
            self.rp = (b >> 4) & 3
            self.opc = self.opc + bytes([b])
            try:
                s = self.instr[self.opc]()
            except KeyError:
                print("Illegal opcode")

#        print(" ".join(["{:02x}".format(b) for b in self.opc]), end=": ")
        return s
