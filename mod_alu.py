#
# Z80 arithmetic and logic instructions
#


from utils import *


class alu:

    def __init__(self, parent):
        self.c = parent

    def addai(self):
        d = self.c.fetch()
        r = add8(self.c.r["A"], d, 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADD A,{:02X}".format(d)

    def addar(self):
        r1s = rname[self.c.r1]
        r = add8(self.c.r["A"], self.c.r[r1s], 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADD A,{:s}".format(r1s)

    def addax(self):
        r1s = rxname[self.c.r1]
        r = add8(self.c.r["A"], self.c.r[r1s], 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADD A,{:s}".format(r1s)

    def adday(self):
        r1s = ryname[self.c.r1]
        r = add8(self.c.r["A"], self.c.r[r1s], 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADD A,{:s}".format(r1s)

    def addam(self):
        d = self.c.rdmem(self.c.r["HL"])
        r = add8(self.c.r["A"], d, 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADD A,(HL)"

    def addamx(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IX"], dsp))
        r = add8(self.c.r["A"], d, 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADD A,(IX+{:02X})".format(dsp)

    def addamy(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IY"], dsp))
        r = add8(self.c.r["A"], d, 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADD A,(IY+{:02X})".format(dsp)

    def adcai(self):
        d = self.c.fetch()
        r = add8(self.c.r["A"], d, self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADC A,{:02X}".format(d)

    def adcar(self):
        r1s = rname[self.c.r1]
        r = add8(self.c.r["A"], self.c.r[r1s], self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADC A,{:s}".format(r1s)

    def adcax(self):
        r1s = rxname[self.c.r1]
        r = add8(self.c.r["A"], self.c.r[r1s], self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADC A,{:s}".format(r1s)

    def adcay(self):
        r1s = ryname[self.c.r1]
        r = add8(self.c.r["A"], self.c.r[r1s], self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADC A,{:s}".format(r1s)

    def adcam(self):
        d = self.c.rdmem(self.c.r["HL"])
        r = add8(self.c.r["A"], d, self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADC A,(HL)"

    def adcamx(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IX"], dsp))
        r = add8(self.c.r["A"], d, self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADC A,(IX+{:02X})".format(dsp)

    def adcamy(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IY"], dsp))
        r = add8(self.c.r["A"], d, self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "ADC A,(IY+{:02X})".format(dsp)

    def subai(self):
        d = self.c.fetch()
        r = sub8(self.c.r["A"], d, 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SUB {:02X}".format(d)

    def subar(self):
        r1s = rname[self.c.r1]
        r = sub8(self.c.r["A"], self.c.r[r1s], 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SUB {:s}".format(r1s)

    def subax(self):
        r1s = rxname[self.c.r1]
        r = sub8(self.c.r["A"], self.c.r[r1s], 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SUB {:s}".format(r1s)

    def subay(self):
        r1s = ryname[self.c.r1]
        r = sub8(self.c.r["A"], self.c.r[r1s], 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SUB {:s}".format(r1s)

    def subam(self):
        d = self.c.rdmem(self.c.r["HL"])
        r = sub8(self.c.r["A"], d, 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SUB (HL)"

    def subamx(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IX"], dsp))
        r = sub8(self.c.r["A"], d, 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SUB (IX+{:02X})".format(dsp)

    def subamy(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IY"], dsp))
        r = sub8(self.c.r["A"], d, 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SUB (IY+{:02X})".format(dsp)

    def sbcai(self):
        d = self.c.fetch()
        r = sub8(self.c.r["A"], d, self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SBC {:02X}".format(d)

    def sbcar(self):
        r1s = rname[self.c.r1]
        r = sub8(self.c.r["A"], self.c.r[r1s], self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SBC {:s}".format(r1s)

    def sbcax(self):
        r1s = rxname[self.c.r1]
        r = sub8(self.c.r["A"], self.c.r[r1s], self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SBC {:s}".format(r1s)

    def sbcay(self):
        r1s = ryname[self.c.r1]
        r = sub8(self.c.r["A"], self.c.r[r1s], self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SBC {:s}".format(r1s)

    def sbcam(self):
        d = self.c.rdmem(self.c.r["HL"])
        r = sub8(self.c.r["A"], d, self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SBC (HL)"

    def sbcamx(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IX"], dsp))
        r = sub8(self.c.r["A"], d, self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SBC (IX+{:02X})".format(dsp)

    def sbcamy(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IY"], dsp))
        r = sub8(self.c.r["A"], d, self.c.r.flag["C"])
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "SBC (IY+{:02X})".format(dsp)

    def andai(self):
        d = self.c.fetch()
        r = lobyte(self.c.r["A"] & d)
        self.c.r["A"] = r
        self.c.r["F"] = logf(r) | 0x10
        return "AND {:02X}".format(d)

    def andar(self):
        r1s = rname[self.c.r1]
        r = lobyte(self.c.r["A"] & self.c.r[r1s])
        self.c.r["A"] = r
        self.c.r["F"] = logf(r) | 0x10
        return "AND {:s}".format(r1s)

    def andax(self):
        r1s = rxname[self.c.r1]
        r = lobyte(self.c.r["A"] & self.c.r[r1s])
        self.c.r["A"] = r
        self.c.r["F"] = logf(r) | 0x10
        return "AND {:s}".format(r1s)

    def anday(self):
        r1s = ryname[self.c.r1]
        r = lobyte(self.c.r["A"] & self.c.r[r1s])
        self.c.r["A"] = r
        self.c.r["F"] = logf(r) | 0x10
        return "AND {:s}".format(r1s)

    def andam(self):
        d = self.c.rdmem(self.c.r["HL"])
        r = lobyte(self.c.r["A"] & d)
        self.c.r["A"] = r
        self.c.r["F"] = logf(r) | 0x10
        return "AND (HL)"

    def andamx(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IX"], dsp))
        r = lobyte(self.c.r["A"] & d)
        self.c.r["A"] = r
        self.c.r["F"] = logf(r) | 0x10
        return "AND (IX+{:02X})".format(dsp)

    def andamy(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IY"], dsp))
        r = lobyte(self.c.r["A"] & d)
        self.c.r["A"] = r
        self.c.r["F"] = logf(r) | 0x10
        return "AND IY+{:02X})".format(dsp)

    def orai(self):
        d = self.c.fetch()
        r = lobyte(self.c.r["A"] | d)
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "OR {:02X}".format(d)

    def orar(self):
        r1s = rname[self.c.r1]
        r = lobyte(self.c.r["A"] | self.c.r[r1s])
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "OR {:s}".format(r1s)

    def orax(self):
        r1s = rxname[self.c.r1]
        r = lobyte(self.c.r["A"] | self.c.r[r1s])
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "OR {:s}".format(r1s)

    def oray(self):
        r1s = ryname[self.c.r1]
        r = lobyte(self.c.r["A"] | self.c.r[r1s])
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "OR {:s}".format(r1s)

    def oram(self):
        d = self.c.rdmem(self.c.r["HL"])
        r = lobyte(self.c.r["A"] | d)
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "OR (HL)"

    def oramx(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IX"], dsp))
        r = lobyte(self.c.r["A"] | d)
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "OR (IX+{:02X})".format(dsp)

    def oramy(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IY"], dsp))
        r = lobyte(self.c.r["A"] | d)
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "OR (IY+{:02X})".format(dsp)

    def xorai(self):
        d = self.c.fetch()
        r = lobyte(self.c.r["A"] ^ d)
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "XOR {:02X}".format(d)

    def xorar(self):
        r1s = rname[self.c.r1]
        r = lobyte(self.c.r["A"] ^ self.c.r[r1s])
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "XOR {:s}".format(r1s)

    def xorax(self):
        r1s = rxname[self.c.r1]
        r = lobyte(self.c.r["A"] ^ self.c.r[r1s])
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "XOR {:s}".format(r1s)

    def xoray(self):
        r1s = ryname[self.c.r1]
        r = lobyte(self.c.r["A"] ^ self.c.r[r1s])
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "XOR {:s}".format(r1s)

    def xoram(self):
        d = self.c.rdmem(self.c.r["HL"])
        r = lobyte(self.c.r["A"] ^ d)
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "XOR (HL)"

    def xoramx(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IX"], dsp))
        r = lobyte(self.c.r["A"] ^ d)
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "XOR (IX+{:02X})".format(dsp)

    def xoramy(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IY"], dsp))
        r = lobyte(self.c.r["A"] ^ d)
        self.c.r["A"] = r
        self.c.r["F"] = logf(r)
        return "XOR (IY+{:02X})".format(dsp)

    def cpai(self):
        d = self.c.fetch()
        r = sub8(self.c.r["A"], d, 0)
        self.c.r["F"] = (r[1] & 0xD7) | (d & 0x28)
        return "CP {:02X}".format(d)

    def cpar(self):
        r1s = rname[self.c.r1]
        d = self.c.r[r1s]
        r = sub8(self.c.r["A"], d, 0)
        self.c.r["F"] = (r[1] & 0xD7) | (d & 0x28)
        return "CP {:s}".format(r1s)

    def cpax(self):
        r1s = rxname[self.c.r1]
        d = self.c.r[r1s]
        r = sub8(self.c.r["A"], d, 0)
        self.c.r["F"] = (r[1] & 0xD7) | (d & 0x28)
        return "CP {:s}".format(r1s)

    def cpay(self):
        r1s = ryname[self.c.r1]
        d = self.c.r[r1s]
        r = sub8(self.c.r["A"], d, 0)
        self.c.r["F"] = (r[1] & 0xD7) | (d & 0x28)
        return "CP {:s}".format(r1s)

    def cpam(self):
        d = self.c.rdmem(self.c.r["HL"])
        r = sub8(self.c.r["A"], d, 0)
        self.c.r["F"] = (r[1] & 0xD7) | (d & 0x28)
        return "CP (HL)"

    def cpamx(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IX"], dsp))
        r = sub8(self.c.r["A"], d, 0)
        self.c.r["F"] = (r[1] & 0xD7) | (d & 0x28)
        return "CP (IX+{:02X})".format(dsp)

    def cpamy(self):
        dsp = self.c.fetch()
        d = self.c.rdmem(adddsp(self.c.r["IY"], dsp))
        r = sub8(self.c.r["A"], d, 0)
        self.c.r["F"] = (r[1] & 0xD7) | (d & 0x28)
        return "CP (IY+{:02X})".format(dsp)

    def addrp(self):
        rps = rpname[self.c.rp]
        r = add16(self.c.r["HL"], self.c.r[rps], 0)
        f = self.c.r["F"] & 0xC4
        self.c.r["HL"] = r[0]
        self.c.r["F"] = f | (r[1] & 0x39)
        return "ADD HL,{:s}".format(rps)

    def addrpx(self):
        rps = rpxname[self.c.rp]
        r = add16(self.c.r["IX"], self.c.r[rps], 0)
        f = self.c.r["F"] & 0xC4
        self.c.r["IX"] = r[0]
        self.c.r["F"] = f | (r[1] & 0x39)
        return "ADD IX,{:s}".format(rps)

    def addrpy(self):
        rps = rpyname[self.c.rp]
        r = add16(self.c.r["IY"], self.c.r[rps], 0)
        f = self.c.r["F"] & 0xC4
        self.c.r["IY"] = r[0]
        self.c.r["F"] = f | (r[1] & 0x39)
        return "ADD IY,{:s}".format(rps)

    def adcrp(self):
        rps = rpname[self.c.rp]
        r = add16(self.c.r["HL"], self.c.r[rps], self.c.r.flag["C"])
        self.c.r["HL"] = r[0]
        self.c.r["F"] = r[1]
        return "ADC HL,{:s}".format(rps)

    def sbcrp(self):
        rps = rpname[self.c.rp]
        r = sub16(self.c.r["HL"], self.c.r[rps], self.c.r.flag["C"])
        self.c.r["HL"] = r[0]
        self.c.r["F"] = r[1]
        return "SBC HL,{:s}".format(rps)

    def daa(self):
        c = 0
        d = self.c.r["A"]
        n = self.c.r.flag["N"]
        if n:
            if self.c.r.flag["C"]:
                d -= 0x60
            if self.c.r.flag["H"]:
                d -= 0x06
        else:
            if self.c.r.flag["C"] or (d > 0x99):
                d += 0x60
                c = 1
            if self.c.r.flag["H"] or ((d & 0x0F) > 0x09):
                d += 0x06

        self.c.r["A"] = d
        self.c.r["F"] = (logf(d) & 0xEC) | c | (n << 1)
        return "DAA"

    def cpla(self):
        d = self.c.r["A"]
        f = (self.c.r["F"] & 0xC5) | 0x12
        f |= (d & 0x28)
        self.c.r["A"] = lobyte(~d)
        self.c.r["F"] = f
        return "CPL"

    def nega(self):
        r = sub8(0, self.c.r["A"], 0)
        self.c.r["A"] = r[0]
        self.c.r["F"] = r[1]
        return "NEG"

    def rla(self):
        d = self.c.r["A"]
        f = self.c.r["F"]
        c = 1 if d & 0x80 else 0
        d = lobyte(d << 1) | (f & 1)
        self.c.r["A"] = d
        self.c.r["F"] = (f & 0xC4) | (d & 0x28) | c
        return "RLA"

    def rra(self):
        d = self.c.r["A"]
        f = self.c.r["F"]
        c = 1 if d & 0x01 else 0
        d = lobyte(d >> 1) | ((f & 1) << 7)
        self.c.r["A"] = d
        self.c.r["F"] = (f & 0xC4) | (d & 0x28) | c
        return "RRA"

    def rlca(self):
        d = self.c.r["A"]
        f = self.c.r["F"]
        c = 1 if d & 0x80 else 0
        d = lobyte(d << 1) | c
        self.c.r["A"] = d
        self.c.r["F"] = (f & 0xC4) | (d & 0x28) | c
        return "RLCA"

    def rrca(self):
        d = self.c.r["A"]
        f = self.c.r["F"]
        c = 1 if d & 0x01 else 0
        d = lobyte(d >> 1) | (c << 7)
        self.c.r["A"] = d
        self.c.r["F"] = (f & 0xC4) | (d & 0x28) | c
        return "RRCA"

    def rrd(self):
        hl = self.c.r["HL"]
        a = self.c.r["A"]
        f = self.c.r["F"]
        d = self.c.rdmem(hl)
        self.c.wrmem(hl, lobyte((d >> 4) | (a << 4)))
        r = (a & 0xF0) | (d & 0x0F)
        self.c.r["A"] = r
        self.c.r["F"] = (f & 1) | (logf(r) & 0xFE)
        return "RRD"

    def rld(self):
        hl = self.c.r["HL"]
        a = self.c.r["A"]
        f = self.c.r["F"]
        d = self.c.rdmem(hl)
        self.c.wrmem(hl, lobyte((d << 4) | (a & 0x0F)))
        r = (a & 0xF0) | ((d >> 4) & 0x0F)
        self.c.r["A"] = r
        self.c.r["F"] = (f & 1) | (logf(r) & 0xFE)
        return "RLD"

    def getinstr(self):
        rv = {}

        # addai, adcai, subai, sbcai
        rv.update({b'\xC6': self.addai})
        rv.update({b'\xdd\xC6': self.addai})
        rv.update({b'\xfd\xC6': self.addai})
        rv.update({b'\xCE': self.adcai})
        rv.update({b'\xdd\xCE': self.adcai})
        rv.update({b'\xfd\xCE': self.adcai})
        rv.update({b'\xD6': self.subai})
        rv.update({b'\xdd\xD6': self.subai})
        rv.update({b'\xfd\xD6': self.subai})
        rv.update({b'\xDE': self.sbcai})
        rv.update({b'\xdd\xDE': self.sbcai})
        rv.update({b'\xfd\xDE': self.sbcai})

        # andai, xorai, orai, cpai
        rv.update({b'\xE6': self.andai})
        rv.update({b'\xdd\xE6': self.andai})
        rv.update({b'\xfd\xE6': self.andai})
        rv.update({b'\xEE': self.xorai})
        rv.update({b'\xdd\xEE': self.xorai})
        rv.update({b'\xfd\xEE': self.xorai})
        rv.update({b'\xF6': self.orai})
        rv.update({b'\xdd\xF6': self.orai})
        rv.update({b'\xfd\xF6': self.orai})
        rv.update({b'\xFE': self.cpai})
        rv.update({b'\xdd\xFE': self.cpai})
        rv.update({b'\xfd\xFE': self.cpai})

        # addar, adcar, subar, sbcar
        for r1 in [0, 1, 2, 3, 4, 5, 7]:
            rv.update({bytes([0x80 | r1]): self.addar})
            rv.update({bytes([0xdd, 0x80 | r1]): self.addax})
            rv.update({bytes([0xfd, 0x80 | r1]): self.adday})
            rv.update({bytes([0x88 | r1]): self.adcar})
            rv.update({bytes([0xdd, 0x88 | r1]): self.adcax})
            rv.update({bytes([0xfd, 0x88 | r1]): self.adcay})
            rv.update({bytes([0x90 | r1]): self.subar})
            rv.update({bytes([0xdd, 0x90 | r1]): self.subax})
            rv.update({bytes([0xfd, 0x90 | r1]): self.subay})
            rv.update({bytes([0x98 | r1]): self.sbcar})
            rv.update({bytes([0xdd, 0x98 | r1]): self.sbcax})
            rv.update({bytes([0xfd, 0x98 | r1]): self.sbcay})

        # andar, xorar, orar, cpar
        for r1 in [0, 1, 2, 3, 4, 5, 7]:
            rv.update({bytes([0xA0 | r1]): self.andar})
            rv.update({bytes([0xdd, 0xA0 | r1]): self.andax})
            rv.update({bytes([0xfd, 0xA0 | r1]): self.anday})
            rv.update({bytes([0xA8 | r1]): self.xorar})
            rv.update({bytes([0xdd, 0xA8 | r1]): self.xorax})
            rv.update({bytes([0xfd, 0xA8 | r1]): self.xoray})
            rv.update({bytes([0xB0 | r1]): self.orar})
            rv.update({bytes([0xdd, 0xB0 | r1]): self.orax})
            rv.update({bytes([0xfd, 0xB0 | r1]): self.oray})
            rv.update({bytes([0xB8 | r1]): self.cpar})
            rv.update({bytes([0xdd, 0xB8 | r1]): self.cpax})
            rv.update({bytes([0xfd, 0xB8 | r1]): self.cpay})

        # addam, addamx, addamy, adcam, adcamx, adcamy
        # subam, subamx, subamy, sbcam, sbcamx, sbcamy
        rv.update({b'\x86': self.addam})
        rv.update({b'\xdd\x86': self.addamx})
        rv.update({b'\xfd\x86': self.addamy})
        rv.update({b'\x8E': self.adcam})
        rv.update({b'\xdd\x8E': self.adcamx})
        rv.update({b'\xfd\x8E': self.adcamy})
        rv.update({b'\x96': self.subam})
        rv.update({b'\xdd\x96': self.subamx})
        rv.update({b'\xfd\x96': self.subamy})
        rv.update({b'\x9E': self.sbcam})
        rv.update({b'\xdd\x9E': self.sbcamx})
        rv.update({b'\xfd\x9E': self.sbcamy})

        # andam, andamx, andamy, xoram, xoramx, xoramy
        # oram, oramx, oramy, cpam, cpamx, cpamy
        rv.update({b'\xA6': self.andam})
        rv.update({b'\xdd\xA6': self.andamx})
        rv.update({b'\xfd\xA6': self.andamy})
        rv.update({b'\xAE': self.xoram})
        rv.update({b'\xdd\xAE': self.xoramx})
        rv.update({b'\xfd\xAE': self.xoramy})
        rv.update({b'\xB6': self.oram})
        rv.update({b'\xdd\xB6': self.oramx})
        rv.update({b'\xfd\xB6': self.oramy})
        rv.update({b'\xBE': self.cpam})
        rv.update({b'\xdd\xBE': self.cpamx})
        rv.update({b'\xfd\xBE': self.cpamy})

        # addrp, addrpx, addrpy, adcrp, sbcrp
        # nega
        for rp in range(4):
            rv.update({bytes([0x09 | (rp << 4)]): self.addrp})
            rv.update({bytes([0xDD, 0x09 | (rp << 4)]): self.addrpx})
            rv.update({bytes([0xFD, 0x09 | (rp << 4)]): self.addrpy})
            rv.update({bytes([0xED, 0x4A | (rp << 4)]): self.adcrp})
            rv.update({bytes([0xED, 0x42 | (rp << 4)]): self.sbcrp})
            rv.update({bytes([0xED, 0x44 | (rp << 4)]): self.nega})
            rv.update({bytes([0xED, 0x4C | (rp << 4)]): self.nega})

        # daa, cpla, rla, rra, rlca, rrca
        rv.update({b'\x27': self.daa})
        rv.update({b'\xdd\x27': self.daa})
        rv.update({b'\xfd\x27': self.daa})
        rv.update({b'\x2f': self.cpla})
        rv.update({b'\xdd\x2f': self.cpla})
        rv.update({b'\xfd\x2f': self.cpla})
        rv.update({b'\x17': self.rla})
        rv.update({b'\xdd\x17': self.rla})
        rv.update({b'\xfd\x17': self.rla})
        rv.update({b'\x07': self.rlca})
        rv.update({b'\xdd\x07': self.rlca})
        rv.update({b'\xfd\x07': self.rlca})
        rv.update({b'\x1f': self.rra})
        rv.update({b'\xdd\x1f': self.rra})
        rv.update({b'\xfd\x1f': self.rra})
        rv.update({b'\x0f': self.rrca})
        rv.update({b'\xdd\x0f': self.rrca})
        rv.update({b'\xfd\x0f': self.rrca})

        # rrd, rld
        rv.update({b'\xed\x67': self.rrd})
        rv.update({b'\xed\x6f': self.rld})

        return rv
