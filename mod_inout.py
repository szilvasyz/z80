#
# Z80 ins, outs
#


from utils import *


class inout:

    def __init__(self, parent):
        self.c = parent

    def ina(self):
        a = self.c.fetch()
        ax = mkword(a, a)
        self.c.r["A"] = self.c.rdinp(ax)
        return "IN A,({:02X})".format(a)

    def outa(self):
        a = self.c.fetch()
        ax = mkword(a, a)
        self.c.wrout(ax, self.c.r["A"])
        return "OUT ({:02X}),A".format(a)

    def inrc(self):
        r0s = rname[self.c.r0]
        a = self.c.r["BC"]
        d = self.c.rdinp(a)
        self.c.r["F"] = (logf(d) & 0xFE) | self.c.r.flag["C"]
        self.c.r[r0s] = d
        return "IN {:s},(C)".format(r0s)

    def in0c(self):
        a = self.c.r["BC"]
        d = self.c.rdinp(a)
        self.c.r["F"] = (logf(d) & 0xFE) | self.c.r.flag["C"]
        return "IN (C)"

    def outcr(self):
        r0s = rname[self.c.r0]
        a = self.c.r["BC"]
        self.c.wrout(a, self.c.r[r0s])
        return "OUT (C),{:s}".format(r0s)

    def outc0(self):
        a = self.c.r["BC"]
        self.c.wrout(a, 0)
        return "OUT (C),0"

    def getinstr(self):
        rv = {}
        for r1 in [0, 1, 2, 3, 4, 5, 7]:
            rv.update({
                bytes([0xED, 0x40 | (r1 << 3)]): self.inrc,
                bytes([0xED, 0x41 | (r1 << 3)]): self.outcr
            })

        # ina, outa
        rv.update({b'\xd3': self.outa})
        rv.update({b'\xdd\xd3': self.outa})
        rv.update({b'\xfd\xd3': self.outa})

        rv.update({b'\xdb': self.ina})
        rv.update({b'\xdd\xdb': self.ina})
        rv.update({b'\xfd\xdb': self.ina})

        # in0c, outc0
        rv.update({b'\xed\x70': self.in0c})
        rv.update({b'\xed\x71': self.outc0})

        return rv

