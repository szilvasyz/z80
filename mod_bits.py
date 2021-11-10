#
# Z80 bit manipulations
#


from utils import *


class bits:

    def __init__(self, parent):
        self.c = parent

    def rlcr(self):
        r1s = rname[self.c.r1]
        d = self.c.r[r1s]
        r = rotfun(d, 0, lambda d, c: [(d << 1) | (d >> 7), d >> 7])
        self.c.r["F"] = r[1]
        self.c.r[r1s] = r[0]
        return "RLC {:s}".format(r1s)

    def rlcm(self):
        a = self.c.r["HL"]
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | (d >> 7), d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "RLC (HL)"

    def rrcr(self):
        r1s = rname[self.c.r1]
        d = self.c.r[r1s]
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (d << 7), d & 1])
        self.c.r["F"] = r[1]
        self.c.r[r1s] = r[0]
        return "RRC {:s}".format(r1s)

    def rrcm(self):
        a = self.c.r["HL"]
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (d << 7), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "RRC (HL)"

    def rlr(self):
        r1s = rname[self.c.r1]
        d = self.c.r[r1s]
        r = rotfun(d, 0, lambda d, c: [(d << 1) | self.c.r.flag["C"], d >> 7])
        self.c.r["F"] = r[1]
        self.c.r[r1s] = r[0]
        return "RL {:s}".format(r1s)

    def rlm(self):
        a = self.c.r["HL"]
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | self.c.r.flag["C"], d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "RL (HL)"

    def rrr(self):
        r1s = rname[self.c.r1]
        d = self.c.r[r1s]
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (self.c.r.flag["C"] << 7), d & 1])
        self.c.r["F"] = r[1]
        self.c.r[r1s] = r[0]
        return "RR {:s}".format(r1s)

    def rrm(self):
        a = self.c.r["HL"]
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (self.c.r.flag["C"] << 7), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "RR (HL)"

    def slar(self):
        r1s = rname[self.c.r1]
        d = self.c.r[r1s]
        r = rotfun(d, 0, lambda d, c: [d << 1, d >> 7])
        self.c.r["F"] = r[1]
        self.c.r[r1s] = r[0]
        return "SLA {:s}".format(r1s)

    def slam(self):
        a = self.c.r["HL"]
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [d << 1, d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "SLA (HL)"

    def srar(self):
        r1s = rname[self.c.r1]
        d = self.c.r[r1s]
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (d & 0x80), d & 1])
        self.c.r["F"] = r[1]
        self.c.r[r1s] = r[0]
        return "SRA {:s}".format(r1s)

    def sram(self):
        a = self.c.r["HL"]
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (d & 0x80), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "SRA (HL)"

    def sllr(self):
        r1s = rname[self.c.r1]
        d = self.c.r[r1s]
        r = rotfun(d, 0, lambda d, c: [(d << 1) | 1, d >> 7])
        self.c.r["F"] = r[1]
        self.c.r[r1s] = r[0]
        return "SLL {:s}".format(r1s)

    def sllm(self):
        a = self.c.r["HL"]
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | 1, d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "SLL (HL)"

    def srlr(self):
        r1s = rname[self.c.r1]
        d = self.c.r[r1s]
        r = rotfun(d, 0, lambda d, c: [(d >> 1), d & 1])
        self.c.r["F"] = r[1]
        self.c.r[r1s] = r[0]
        return "SRL {:s}".format(r1s)

    def srlm(self):
        a = self.c.r["HL"]
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "SRL (HL)"

    def bitnr(self):
        r1s = rname[self.c.r1]
        b = self.c.r0
        d = self.c.r[r1s] & (1 << b)
        self.c.r["F"] = logf(d) | self.c.r.flag["C"]
        return "BIT {:d},{:s}".format(b, r1s)

    def bitnm(self):
        a = self.c.r["HL"]
        b = self.c.r0
        d = self.c.rdmem(a) & (1 << b)
        self.c.r["F"] = logf(d) | self.c.r.flag["C"]
        return "BIT {:d},(HL)".format(b)

    def resnr(self):
        r1s = rname[self.c.r1]
        b = self.c.r0
        self.c.r[r1s] = self.c.r[r1s] & ~(1 << b)
        return "RES {:d},{:s}".format(b, r1s)

    def resnm(self):
        a = self.c.r["HL"]
        b = self.c.r0
        self.c.wrmem(a, self.c.rdmem(a) & ~(1 << b))
        return "RES {:d},(HL)".format(b)

    def setnr(self):
        r1s = rname[self.c.r1]
        b = self.c.r0
        self.c.r[r1s] = self.c.r[r1s] | (1 << b)
        return "SET {:d},{:s}".format(b, r1s)

    def setnm(self):
        a = self.c.r["HL"]
        b = self.c.r0
        self.c.wrmem(a, self.c.rdmem(a) | (1 << b))
        return "SET {:d},(HL)".format(b)

    def rlcmxr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | (d >> 7), d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "RLC (IX+{:02X}),{:s}".format(self.c.dsp, r1s)

    def rlcmx(self):
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | (d >> 7), d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "RLC (IX+{:02X})".format(self.c.dsp)

    def rlcmyr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | (d >> 7), d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "RLC (IY+{:02X}),{:s}".format(self.c.dsp, r1s)

    def rlcmy(self):
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | (d >> 7), d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "RLC (IY+{:02X})".format(self.c.dsp)

    def rrcmxr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (d << 7), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "RRC (IX+{:02X}),{:s}".format(self.c.dsp, r1s)

    def rrcmx(self):
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (d << 7), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "RRC (IX+{:02X})".format(self.c.dsp)

    def rrcmyr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (d << 7), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "RRC (IY+{:02X}),{:s}".format(self.c.dsp, r1s)

    def rrcmy(self):
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (d << 7), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "RRC (IY+{:02X})".format(self.c.dsp)

    def rlmxr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | self.c.r.flag["C"], d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "RL (IX+{:02X}),{:s}".format(self.c.dsp, r1s)

    def rlmx(self):
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | self.c.r.flag["C"], d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "RL (IX+{:02X})".format(self.c.dsp)

    def rlmyr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | self.c.r.flag["C"], d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "RL (IY+{:02X}),{:s}".format(self.c.dsp, r1s)

    def rlmy(self):
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | self.c.r.flag["C"], d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "RL (IY+{:02X})".format(self.c.dsp)

    def rrmxr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (self.c.r.flag["C"] << 7), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "RR (IX+{:02X}),{:s}".format(self.c.dsp, r1s)

    def rrmx(self):
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (self.c.r.flag["C"] << 7), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "RR (IX+{:02X})".format(self.c.dsp)

    def rrmyr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (self.c.r.flag["C"] << 7), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "RR (IY+{:02X}),{:s}".format(self.c.dsp, r1s)

    def rrmy(self):
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (self.c.r.flag["C"] << 7), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "RR (IY+{:02X})".format(self.c.dsp)

    def slamxr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [d << 1, d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "SLA (IX+{:02X}),{:s}".format(self.c.dsp, r1s)

    def slamx(self):
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [d << 1, d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "SLA (IX+{:02X})".format(self.c.dsp)

    def slamyr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [d << 1, d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "SLA (IY+{:02X}),{:s}".format(self.c.dsp, r1s)

    def slamy(self):
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [d << 1, d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "SLA (IY+{:02X})".format(self.c.dsp)

    def sramxr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (d & 0x80), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "SLA (IX+{:02X}),{:s}".format(self.c.dsp, r1s)

    def sramx(self):
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (d & 0x80), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "SRA (IX+{:02X})".format(self.c.dsp)

    def sramyr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (d & 0x80), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "SRA (IY+{:02X}),{:s}".format(self.c.dsp, r1s)

    def sramy(self):
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1) | (d & 0x80), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "SRA (IY+{:02X})".format(self.c.dsp)

    def sllmxr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | 1, d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "SLL (IX+{:02X}),{:s}".format(self.c.dsp, r1s)

    def sllmx(self):
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | 1, d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "SLL (IX+{:02X})".format(self.c.dsp)

    def sllmyr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | 1, d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "SLL (IY+{:02X}),{:s}".format(self.c.dsp, r1s)

    def sllmy(self):
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d << 1) | 1, d >> 7])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "SLL (IY+{:02X})".format(self.c.dsp)

    def srlmxr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "SRL (IX+{:02X}),{:s}".format(self.c.dsp, r1s)

    def srlmx(self):
        a = adddsp(self.c.r["IX"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "SRL (IX+{:02X})".format(self.c.dsp)

    def srlmyr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        self.c.r[r1s] = r[0]
        return "SRL (IY+{:02X}),{:s}".format(self.c.dsp, r1s)

    def srlmy(self):
        a = adddsp(self.c.r["IY"], self.c.dsp)
        d = self.c.rdmem(a)
        r = rotfun(d, 0, lambda d, c: [(d >> 1), d & 1])
        self.c.r["F"] = r[1]
        self.c.wrmem(a, r[0])
        return "SRL (IY+{:02X})".format(self.c.dsp)

    def bitnmx(self):
        a = adddsp(self.c.r["IX"], self.c.dsp)
        b = self.c.r0
        d = self.c.rdmem(a) & (1 << b)
        self.c.r["F"] = logf(d) | self.c.r.flag["C"]
        return "BIT {:d},(IX+{:02X})".format(b, self.c.dsp)

    def bitnmy(self):
        a = adddsp(self.c.r["IY"], self.c.dsp)
        b = self.c.r0
        d = self.c.rdmem(a) & (1 << b)
        self.c.r["F"] = logf(d) | self.c.r.flag["C"]
        return "BIT {:d},(IY+{:02X})".format(b, self.c.dsp)

    def resnmxr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IX"], self.c.dsp)
        b = self.c.r0
        d = self.c.rdmem(a)
        d = d & ~(1 << b)
        self.c.wrmem(a, d)
        self.c.r[r1s] = d
        return "RES {:d},(IX+{:02X}),{:s}".format(b, self.c.dsp, r1s)

    def resnmx(self):
        a = adddsp(self.c.r["IX"], self.c.dsp)
        b = self.c.r0
        d = self.c.rdmem(a)
        d = d & ~(1 << b)
        self.c.wrmem(a, d)
        return "RES {:d},(IX+{:02X})".format(b, self.c.dsp)

    def resnmyr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IY"], self.c.dsp)
        b = self.c.r0
        d = self.c.rdmem(a)
        d = d & ~(1 << b)
        self.c.wrmem(a, d)
        self.c.r[r1s] = d
        return "RES {:d},(IY+{:02X}),{:s}".format(b, self.c.dsp, r1s)

    def resnmy(self):
        a = adddsp(self.c.r["IY"], self.c.dsp)
        b = self.c.r0
        d = self.c.rdmem(a)
        d = d & ~(1 << b)
        self.c.wrmem(a, d)
        return "RES {:d},(IY+{:02X})".format(b, self.c.dsp)

    def setnmxr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IX"], self.c.dsp)
        b = self.c.r0
        d = self.c.rdmem(a)
        d = d | (1 << b)
        self.c.wrmem(a, d)
        self.c.r[r1s] = d
        return "SET {:d},(IX+{:02X}),{:s}".format(b, self.c.dsp, r1s)

    def setnmx(self):
        a = adddsp(self.c.r["IX"], self.c.dsp)
        b = self.c.r0
        d = self.c.rdmem(a)
        d = d | (1 << b)
        self.c.wrmem(a, d)
        return "SET {:d},(IX+{:02X})".format(b, self.c.dsp)

    def setnmyr(self):
        r1s = rname[self.c.r1]
        a = adddsp(self.c.r["IY"], self.c.dsp)
        b = self.c.r0
        d = self.c.rdmem(a)
        d = d | (1 << b)
        self.c.wrmem(a, d)
        self.c.r[r1s] = d
        return "SET {:d},(IY+{:02X}),{:s}".format(b, self.c.dsp, r1s)

    def setnmy(self):
        a = adddsp(self.c.r["IY"], self.c.dsp)
        b = self.c.r0
        d = self.c.rdmem(a)
        d = d | (1 << b)
        self.c.wrmem(a, d)
        return "SET {:d},(IY+{:02X})".format(b, self.c.dsp)

    def getinstr(self):
        rv = {}

        # rlcr, rrcr, rlr, rrr
        # slar, srar, sllr, srlr
        for r1 in [0, 1, 2, 3, 4, 5, 7]:
            rv.update({bytes([0xCB, 0x00 | r1]): self.rlcr})
            rv.update({bytes([0xCB, 0x08 | r1]): self.rrcr})
            rv.update({bytes([0xCB, 0x10 | r1]): self.rlr})
            rv.update({bytes([0xCB, 0x18 | r1]): self.rrr})
            rv.update({bytes([0xCB, 0x20 | r1]): self.slar})
            rv.update({bytes([0xCB, 0x28 | r1]): self.srar})
            rv.update({bytes([0xCB, 0x30 | r1]): self.sllr})
            rv.update({bytes([0xCB, 0x38 | r1]): self.srlr})

        # rlcm, rrcm, rlm, rrm
        # slam, sram, sllm, srlm
        rv.update({bytes([0xCB, 0x06]): self.rlcm})
        rv.update({bytes([0xCB, 0x0E]): self.rrcm})
        rv.update({bytes([0xCB, 0x16]): self.rlm})
        rv.update({bytes([0xCB, 0x1E]): self.rrm})
        rv.update({bytes([0xCB, 0x26]): self.slam})
        rv.update({bytes([0xCB, 0x2E]): self.sram})
        rv.update({bytes([0xCB, 0x36]): self.sllm})
        rv.update({bytes([0xCB, 0x3E]): self.srlm})

        # bitnr, bitnm, resnr, resnm, setnr, setnm
        for r0 in range(8):
            for r1 in [0, 1, 2, 3, 4, 5, 7]:
                rv.update({bytes([0xCB, 0x40 | (r0 << 3) | r1]): self.bitnr})
                rv.update({bytes([0xCB, 0x80 | (r0 << 3) | r1]): self.resnr})
                rv.update({bytes([0xCB, 0xC0 | (r0 << 3) | r1]): self.setnr})

            rv.update({bytes([0xCB, 0x46 | (r0 << 3)]): self.bitnm})
            rv.update({bytes([0xCB, 0x86 | (r0 << 3)]): self.resnm})
            rv.update({bytes([0xCB, 0xC6 | (r0 << 3)]): self.setnm})

        # rlcmxr, rrcmxr, rlmxr, rrmxr
        # slamxr, sramxr, sllmxr, srlmxr
        for r1 in [0, 1, 2, 3, 4, 5, 7]:
            rv.update({bytes([0xDD, 0xCB, 0x00 | r1]): self.rlcmxr})
            rv.update({bytes([0xDD, 0xCB, 0x08 | r1]): self.rrcmxr})
            rv.update({bytes([0xDD, 0xCB, 0x10 | r1]): self.rlmxr})
            rv.update({bytes([0xDD, 0xCB, 0x18 | r1]): self.rrmxr})
            rv.update({bytes([0xDD, 0xCB, 0x20 | r1]): self.slamxr})
            rv.update({bytes([0xDD, 0xCB, 0x28 | r1]): self.sramxr})
            rv.update({bytes([0xDD, 0xCB, 0x30 | r1]): self.sllmxr})
            rv.update({bytes([0xDD, 0xCB, 0x38 | r1]): self.srlmxr})
            rv.update({bytes([0xFD, 0xCB, 0x00 | r1]): self.rlcmyr})
            rv.update({bytes([0xFD, 0xCB, 0x08 | r1]): self.rrcmyr})
            rv.update({bytes([0xFD, 0xCB, 0x10 | r1]): self.rlmyr})
            rv.update({bytes([0xFD, 0xCB, 0x18 | r1]): self.rrmyr})
            rv.update({bytes([0xFD, 0xCB, 0x20 | r1]): self.slamyr})
            rv.update({bytes([0xFD, 0xCB, 0x28 | r1]): self.sramyr})
            rv.update({bytes([0xFD, 0xCB, 0x30 | r1]): self.sllmyr})
            rv.update({bytes([0xFD, 0xCB, 0x38 | r1]): self.srlmyr})

        # rlcmx, rlcmy, rrcmx, rrcmy, rlmx, rlmy, rrmx, rrmy
        # slamx, slamy, sramx, sramy, sllmx, sllmy, srlmx, srlmy
        rv.update({bytes([0xDD, 0xCB, 0x06]): self.rlcmx})
        rv.update({bytes([0xDD, 0xCB, 0x0E]): self.rrcmx})
        rv.update({bytes([0xDD, 0xCB, 0x16]): self.rlmx})
        rv.update({bytes([0xDD, 0xCB, 0x1E]): self.rrmx})
        rv.update({bytes([0xDD, 0xCB, 0x26]): self.slamx})
        rv.update({bytes([0xDD, 0xCB, 0x2E]): self.sramx})
        rv.update({bytes([0xDD, 0xCB, 0x36]): self.sllmx})
        rv.update({bytes([0xDD, 0xCB, 0x3E]): self.srlmx})
        rv.update({bytes([0xFD, 0xCB, 0x06]): self.rlcmy})
        rv.update({bytes([0xFD, 0xCB, 0x0E]): self.rrcmy})
        rv.update({bytes([0xFD, 0xCB, 0x16]): self.rlmy})
        rv.update({bytes([0xFD, 0xCB, 0x1E]): self.rrmy})
        rv.update({bytes([0xFD, 0xCB, 0x26]): self.slamy})
        rv.update({bytes([0xFD, 0xCB, 0x2E]): self.sramy})
        rv.update({bytes([0xFD, 0xCB, 0x36]): self.sllmy})
        rv.update({bytes([0xFD, 0xCB, 0x3E]): self.srlmy})

        # bitnmx, bitnmy, resnxr, resnmyr,
        # resnmx, resnmy, setnmxr, setnmyr, setnmx, setnmy
        for r0 in range(8):
            for r1 in [0, 1, 2, 3, 4, 5, 7]:
                rv.update({bytes([0xDD, 0xCB, 0x40 | (r0 << 3) | r1]): self.bitnmx})
                rv.update({bytes([0xDD, 0xCB, 0x80 | (r0 << 3) | r1]): self.resnmxr})
                rv.update({bytes([0xDD, 0xCB, 0xC0 | (r0 << 3) | r1]): self.setnmxr})
                rv.update({bytes([0xFD, 0xCB, 0x40 | (r0 << 3) | r1]): self.bitnmy})
                rv.update({bytes([0xFD, 0xCB, 0x80 | (r0 << 3) | r1]): self.resnmyr})
                rv.update({bytes([0xFD, 0xCB, 0xC0 | (r0 << 3) | r1]): self.setnmyr})

            rv.update({bytes([0xDD, 0xCB, 0x46 | (r0 << 3)]): self.bitnmx})
            rv.update({bytes([0xDD, 0xCB, 0x86 | (r0 << 3)]): self.resnmx})
            rv.update({bytes([0xDD, 0xCB, 0xC6 | (r0 << 3)]): self.setnmx})
            rv.update({bytes([0xFD, 0xCB, 0x46 | (r0 << 3)]): self.bitnmy})
            rv.update({bytes([0xFD, 0xCB, 0x86 | (r0 << 3)]): self.resnmy})
            rv.update({bytes([0xFD, 0xCB, 0xC6 | (r0 << 3)]): self.setnmy})

        return rv
