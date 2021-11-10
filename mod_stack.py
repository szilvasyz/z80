#
# Z80 pushes, pops, calls, rets
#


from utils import *


class stack:

    def __init__(self, parent):
        self.c = parent

    def push(self):
        rps = rp2name[self.c.rp]
        self.c.push(self.c.r[rps])
        return "PUSH {:s}".format(rps)

    def pushx(self):
        rps = rp2xname[self.c.rp]
        self.c.push(self.c.r[rps])
        return "PUSH {:s}".format(rps)

    def pushy(self):
        rps = rp2yname[self.c.rp]
        self.c.push(self.c.r[rps])
        return "PUSH {:s}".format(rps)

    def pop(self):
        rps = rp2name[self.c.rp]
        self.c.r[rps] = self.c.pop()
        return "POP {:s}".format(rps)

    def popx(self):
        rps = rp2xname[self.c.rp]
        self.c.r[rps] = self.c.pop()
        return "POP {:s}".format(rps)

    def popy(self):
        rps = rp2yname[self.c.rp]
        self.c.r[rps] = self.c.pop()
        return "POP {:s}".format(rps)

    def call(self):
        a = self.c.fetch16()
        self.c.push(self.c.r["PC"])
        self.c.r["PC"] = a
        return "CALL {:04X}".format(a)

    def ret(self):
        a = self.c.pop()
        self.c.r["PC"] = a
        return "RET"

    def reti(self):
        a = self.c.pop()
        self.c.r["PC"] = a
        return "RETI"

    def retn(self):
        a = self.c.pop()
        self.c.r["PC"] = a
        self.c.iff1 = self.c.iff2
        return "RETN"

    def callnz(self):
        a = self.c.fetch16()
        if not self.c.r.flag["Z"]:
            self.c.push(self.c.r["PC"])
            self.c.r["PC"] = a
        return "CALL NZ,{:04X}".format(a)

    def callz(self):
        a = self.c.fetch16()
        if self.c.r.flag["Z"]:
            self.c.push(self.c.r["PC"])
            self.c.r["PC"] = a
        return "CALL Z,{:04X}".format(a)

    def callnc(self):
        a = self.c.fetch16()
        if not self.c.r.flag["C"]:
            self.c.push(self.c.r["PC"])
            self.c.r["PC"] = a
        return "CALL NC,{:04X}".format(a)

    def callc(self):
        a = self.c.fetch16()
        if self.c.r.flag["C"]:
            self.c.push(self.c.r["PC"])
            self.c.r["PC"] = a
        return "CALL C,{:04X}".format(a)

    def callpo(self):
        a = self.c.fetch16()
        if not self.c.r.flag["P"]:
            self.c.push(self.c.r["PC"])
            self.c.r["PC"] = a
        return "CALL PO,{:04X}".format(a)

    def callpe(self):
        a = self.c.fetch16()
        if self.c.r.flag["P"]:
            self.c.push(self.c.r["PC"])
            self.c.r["PC"] = a
        return "CALL PE,{:04X}".format(a)

    def callp(self):
        a = self.c.fetch16()
        if not self.c.r.flag["S"]:
            self.c.push(self.c.r["PC"])
            self.c.r["PC"] = a
        return "CALL P,{:04X}".format(a)

    def callm(self):
        a = self.c.fetch16()
        if self.c.r.flag["S"]:
            self.c.push(self.c.r["PC"])
            self.c.r["PC"] = a
        return "CALL M,{:04X}".format(a)
        return

    def retnz(self):
        if not self.c.r.flag["Z"]:
            a = self.c.pop()
            self.c.r["PC"] = a
        return "RET NZ"

    def retz(self):
        if self.c.r.flag["Z"]:
            a = self.c.pop()
            self.c.r["PC"] = a
        return "RET Z"

    def retnc(self):
        if not self.c.r.flag["C"]:
            a = self.c.pop()
            self.c.r["PC"] = a
        return "RET NC"

    def retc(self):
        if self.c.r.flag["C"]:
            a = self.c.pop()
            self.c.r["PC"] = a
        return "RET C"

    def retpo(self):
        if not self.c.r.flag["P"]:
            a = self.c.pop()
            self.c.r["PC"] = a
        return "RET PO"

    def retpe(self):
        if self.c.r.flag["P"]:
            a = self.c.pop()
            self.c.r["PC"] = a
        return "RET PE"

    def retp(self):
        if not self.c.r.flag["S"]:
            a = self.c.pop()
            self.c.r["PC"] = a
        return "RET P"

    def retm(self):
        if self.c.r.flag["S"]:
            a = self.c.pop()
            self.c.r["PC"] = a
        return "RET M"

    def rst(self):
        a = self.c.r0 << 3
        self.c.push(self.c.r["PC"])
        self.c.r["PC"] = a
        return "RST {:02X}".format(a)

    def getinstr(self):
        rv = {}
        for rp in range(4):
            rv.update({
                bytes([0xC5 | (rp << 4)]): self.push,
                bytes([0xDD, 0xC5 | (rp << 4)]): self.push,
                bytes([0xFD, 0xC5 | (rp << 4)]): self.push,
                bytes([0xC1 | (rp << 4)]): self.pop,
                bytes([0xDD, 0xC1 | (rp << 4)]): self.pop,
                bytes([0xFD, 0xC1 | (rp << 4)]): self.pop
            })

        rv.update({b'\xdd\xe5': self.pushx})
        rv.update({b'\xdd\xe1': self.popx})

        rv.update({b'\xfd\xe5': self.pushy})
        rv.update({b'\xfd\xe1': self.popy})

        rv.update({b'\xcd': self.call})
        rv.update({b'\xdd\xcd': self.call})
        rv.update({b'\xfd\xcd': self.call})
        rv.update({b'\xc9': self.ret})
        rv.update({b'\xdd\xc9': self.ret})
        rv.update({b'\xfd\xc9': self.ret})

        rv.update({b'\xc4': self.callnz})
        rv.update({b'\xdd\xc4': self.callnz})
        rv.update({b'\xfd\xc4': self.callnz})
        rv.update({b'\xcc': self.callz})
        rv.update({b'\xdd\xcc': self.callz})
        rv.update({b'\xfd\xcc': self.callz})

        rv.update({b'\xd4': self.callnc})
        rv.update({b'\xdd\xd4': self.callnc})
        rv.update({b'\xfd\xd4': self.callnc})
        rv.update({b'\xdc': self.callc})
        rv.update({b'\xdd\xdc': self.callc})
        rv.update({b'\xfd\xdc': self.callc})

        rv.update({b'\xe4': self.callpo})
        rv.update({b'\xdd\xe4': self.callpo})
        rv.update({b'\xfd\xe4': self.callpo})
        rv.update({b'\xec': self.callpe})
        rv.update({b'\xdd\xec': self.callpe})
        rv.update({b'\xfd\xec': self.callpe})

        rv.update({b'\xf4': self.callp})
        rv.update({b'\xdd\xf4': self.callp})
        rv.update({b'\xfd\xf4': self.callp})
        rv.update({b'\xfc': self.callm})
        rv.update({b'\xdd\xfc': self.callm})
        rv.update({b'\xfd\xfc': self.callm})

        rv.update({b'\xc0': self.retnz})
        rv.update({b'\xdd\xc0': self.retnz})
        rv.update({b'\xfd\xc0': self.retnz})
        rv.update({b'\xc8': self.retz})
        rv.update({b'\xdd\xc8': self.retz})
        rv.update({b'\xfd\xc8': self.retz})

        rv.update({b'\xd0': self.retnc})
        rv.update({b'\xdd\xd0': self.retnc})
        rv.update({b'\xfd\xd0': self.retnc})
        rv.update({b'\xd8': self.retc})
        rv.update({b'\xdd\xd8': self.retc})
        rv.update({b'\xfd\xd8': self.retc})

        rv.update({b'\xe0': self.retpo})
        rv.update({b'\xdd\xe0': self.retpo})
        rv.update({b'\xfd\xe0': self.retpo})
        rv.update({b'\xe8': self.retpe})
        rv.update({b'\xdd\xe8': self.retpe})
        rv.update({b'\xfd\xe8': self.retpe})

        rv.update({b'\xf0': self.retp})
        rv.update({b'\xdd\xf0': self.retp})
        rv.update({b'\xfd\xf0': self.retp})
        rv.update({b'\xf8': self.retm})
        rv.update({b'\xdd\xf8': self.retm})
        rv.update({b'\xfd\xf8': self.retm})

        for r0 in range(8):
            rv.update({bytes([0xC7 | (r0 << 3)]): self.rst})
            rv.update({bytes([0xDD, 0xC7 | (r0 << 3)]): self.rst})
            rv.update({bytes([0xFD, 0xC7 | (r0 << 3)]): self.rst})
            rv.update({bytes([0xED, 0x45 | (r0 << 3)]): self.retn})

        rv.update({b'\xED\x4D': self.reti})

        return rv

