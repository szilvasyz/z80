#
# Z80 increments/decrements
#


from utils import *


class incdec:

    def __init__(self, parent):
        self.c = parent

    def incr(self):
        r0s = rname[self.c.r0]
        f = self.c.r["F"] & 1
        r = add8(self.c.r[r0s], 1, 0)
        self.c.r[r0s] = r[0]
        self.c.r["F"] = f | (r[1] & 0xFE)
        return "INC {:s}".format(r0s)

    def incrx(self):
        r0s = rxname[self.c.r0]
        f = self.c.r["F"] & 1
        r = add8(self.c.r[r0s], 1, 0)
        self.c.r[r0s] = r[0]
        self.c.r["F"] = f | (r[1] & 0xFE)
        return "INC {:s}".format(r0s)

    def incry(self):
        r0s = ryname[self.c.r0]
        f = self.c.r["F"] & 1
        r = add8(self.c.r[r0s], 1, 0)
        self.c.r[r0s] = r[0]
        self.c.r["F"] = f | (r[1] & 0xFE)
        return "INC {:s}".format(r0s)

    def incm(self):
        a = self.c.r["HL"]
        f = self.c.r["F"] & 1
        r = add8(self.c.rdmem(a), 1, 0)
        self.c.wrmem(a, r[0])
        self.c.r["F"] = f | (r[1] & 0xFE)
        return "INC (HL)"

    def incmx(self):
        dsp = self.c.fetch()
        a = adddsp(self.c.r["IX"], dsp)
        f = self.c.r["F"] & 1
        r = add8(self.c.rdmem(a), 1, 0)
        self.c.wrmem(a, r[0])
        self.c.r["F"] = f | (r[1] & 0xFE)
        return "INC (IX+{:02X})".format(dsp)

    def incmy(self):
        dsp = self.c.fetch()
        a = adddsp(self.c.r["IY"], dsp)
        f = self.c.r["F"] & 1
        r = add8(self.c.rdmem(a), 1, 0)
        self.c.wrmem(a, r[0])
        self.c.r["F"] = f | (r[1] & 0xFE)
        return "INC (IY+{:02X})".format(dsp)

    def decr(self):
        r0s = rname[self.c.r0]
        f = self.c.r["F"] & 1
        r = sub8(self.c.r[r0s], 1, 0)
        self.c.r[r0s] = r[0]
        self.c.r["F"] = f | (r[1] & 0xFE)
        return "DEC {:s}".format(r0s)

    def decrx(self):
        r0s = rxname[self.c.r0]
        f = self.c.r["F"] & 1
        r = sub8(self.c.r[r0s], 1, 0)
        self.c.r[r0s] = r[0]
        self.c.r["F"] = f | (r[1] & 0xFE)
        return "DEC {:s}".format(r0s)

    def decry(self):
        r0s = ryname[self.c.r0]
        f = self.c.r["F"] & 1
        r = sub8(self.c.r[r0s], 1, 0)
        self.c.r[r0s] = r[0]
        self.c.r["F"] = f | (r[1] & 0xFE)
        return "DEC {:s}".format(r0s)

    def decm(self):
        a = self.c.r["HL"]
        f = self.c.r["F"] & 1
        r = add8(self.c.rdmem(a), 1, 0)
        self.c.wrmem(a, r[0])
        self.c.r["F"] = f | (r[1] & 0xFE)
        return "DEC (HL)"

    def decmx(self):
        dsp = self.c.fetch()
        a = adddsp(self.c.r["IX"], dsp)
        f = self.c.r["F"] & 1
        r = add8(self.c.rdmem(a), 1, 0)
        self.c.wrmem(a, r[0])
        self.c.r["F"] = f | (r[1] & 0xFE)
        return "DEC (IX+{:02X})".format(dsp)

    def decmy(self):
        dsp = self.c.fetch()
        a = adddsp(self.c.r["IY"], dsp)
        f = self.c.r["F"] & 1
        r = add8(self.c.rdmem(a), 1, 0)
        self.c.wrmem(a, r[0])
        self.c.r["F"] = f | (r[1] & 0xFE)
        return "DEC (IY+{:02X})".format(dsp)

    def incrp(self):
        rp = rpname[self.c.rp]
        d = word(self.c.r[rp] + 1)
        self.c.r[rp] = d
        return "INC {:s}".format(rp)

    def incrpx(self):
        rp = rpxname[self.c.rp]
        d = word(self.c.r[rp] + 1)
        self.c.r[rp] = d
        return "INC {:s}".format(rp)

    def incrpy(self):
        rp = rpyname[self.c.rp]
        d = word(self.c.r[rp] + 1)
        self.c.r[rp] = d
        return "INC {:s}".format(rp)

    def decrp(self):
        rp = rpname[self.c.rp]
        d = word(self.c.r[rp] - 1)
        self.c.r[rp] = d
        return "DEC {:s}".format(rp)

    def decrpx(self):
        rp = rpxname[self.c.rp]
        d = word(self.c.r[rp] - 1)
        self.c.r[rp] = d
        return "DEC{:s}".format(rp)

    def decrpy(self):
        rp = rpyname[self.c.rp]
        d = word(self.c.r[rp] - 1)
        self.c.r[rp] = d
        return "DEC{:s}".format(rp)

    def getinstr(self):
        rv = {}

        # incr, incrx, incry, decr, decrx, decry
        for r1 in [0, 1, 2, 3, 4, 5, 7]:
            rv.update({bytes([0x04 | (r1 << 3)]): self.incr})
            rv.update({bytes([0xDD, 0x04 | (r1 << 3)]): self.incrx})
            rv.update({bytes([0xFD, 0x04 | (r1 << 3)]): self.incry})
            rv.update({bytes([0x05 | (r1 << 3)]): self.decr})
            rv.update({bytes([0xDD, 0x05 | (r1 << 3)]): self.decrx})
            rv.update({bytes([0xFD, 0x05 | (r1 << 3)]): self.decry})

        # incm, incmx, decm, decmx
        rv.update({b'\x34': self.incm})
        rv.update({b'\xdd\x34': self.incmx})
        rv.update({b'\xfd\x34': self.incmy})
        rv.update({b'\x35': self.decm})
        rv.update({b'\xdd\x35': self.decmx})
        rv.update({b'\xfd\x35': self.decmy})

        # incrp, incrpx, incrpy
        # decrp, decrpx, decrpy
        for rp in range(4):
            rv.update({bytes([0x03 | (rp << 4)]): self.incrp})
            rv.update({bytes([0xDD, 0x03 | (rp << 4)]): self.incrpx})
            rv.update({bytes([0xFD, 0x03 | (rp << 4)]): self.incrpy})
            rv.update({bytes([0x0B | (rp << 4)]): self.decrp})
            rv.update({bytes([0xDD, 0x0B | (rp << 4)]): self.decrpx})
            rv.update({bytes([0xFD, 0x0B | (rp << 4)]): self.decrpy})

        return rv
