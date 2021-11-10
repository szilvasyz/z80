#
# Z80 block instructions
#


from utils import *


class block:

    def __init__(self, parent):
        self.c = parent

    def ldi(self):
        bc = word(self.c.r["BC"] - 1)
        de = self.c.r["DE"]
        hl = self.c.r["HL"]
        d = self.c.rdmem(hl)
        self.c.wrmem(de, d)
        self.c.r["HL"] = word(hl + 1)
        self.c.r["DE"] = word(de + 1)
        self.c.r["BC"] = bc
        d += self.c.r["A"]
        f = self.c.r["F"] & 0xC1
        f |= ((d & 0x02) << 4) | (d & 0x08)
        f |= 0x04 if bc else 0
        self.c.r["F"] = f
        return "LDI"

    def ldir(self):
        bc = word(self.c.r["BC"] - 1)
        de = self.c.r["DE"]
        hl = self.c.r["HL"]
        d = self.c.rdmem(hl)
        self.c.wrmem(de, d)
        self.c.r["HL"] = word(hl + 1)
        self.c.r["DE"] = word(de + 1)
        self.c.r["BC"] = bc
        d += self.c.r["A"]
        f = self.c.r["F"] & 0xC1
        f |= ((d & 0x02) << 4) | (d & 0x08)
        f |= 0x04 if bc else 0
        self.c.r["F"] = f
        if bc:
            self.c.r["PC"] = word(self.c.r["PC"] - 2)
        return "LDIR"

    def ldd(self):
        bc = word(self.c.r["BC"] - 1)
        de = self.c.r["DE"]
        hl = self.c.r["HL"]
        d = self.c.rdmem(hl)
        self.c.wrmem(de, d)
        self.c.r["HL"] = word(hl - 1)
        self.c.r["DE"] = word(de - 1)
        self.c.r["BC"] = bc
        d += self.c.r["A"]
        f = self.c.r["F"] & 0xC1
        f |= ((d & 0x02) << 4) | (d & 0x08)
        f |= 0x04 if bc else 0
        self.c.r["F"] = f
        return "LDD"

    def lddr(self):
        bc = word(self.c.r["BC"] - 1)
        de = self.c.r["DE"]
        hl = self.c.r["HL"]
        d = self.c.rdmem(hl)
        self.c.wrmem(de, d)
        self.c.r["HL"] = word(hl - 1)
        self.c.r["DE"] = word(de - 1)
        self.c.r["BC"] = bc
        d += self.c.r["A"]
        f = self.c.r["F"] & 0xC1
        f |= ((d & 0x02) << 4) | (d & 0x08)
        f |= 0x04 if bc else 0
        self.c.r["F"] = f
        if bc:
            self.c.r["PC"] = word(self.c.r["PC"] - 2)
        return "LDDR"

    def cpi(self):
        bc = word(self.c.r["BC"] - 1)
        hl = self.c.r["HL"]
        r = sub8(self.c.r["A"], self.c.rdmem(hl), 0)
        t = r[0] - ((r[1] & 0x10) >> 4)
        f = 0x02 | (0x04 if bc else 0)
        f |= (t & 0x08) | ((t & 0x02) >> 4) | self.c.r.flag["C"]
        self.c.r["F"] = (r[1] & 0xD0) | f
        self.c.r["HL"] = word(hl + 1)
        self.c.r["BC"] = bc
        return "CPI"

    def cpir(self):
        bc = word(self.c.r["BC"] - 1)
        hl = self.c.r["HL"]
        r = sub8(self.c.r["A"], self.c.rdmem(hl), 0)
        t = r[0] - ((r[1] & 0x10) >> 4)
        f = 0x02 | (0x04 if bc else 0)
        f |= (t & 0x08) | ((t & 0x02) >> 4) | self.c.r.flag["C"]
        self.c.r["F"] = (r[1] & 0xD0) | f
        self.c.r["HL"] = word(hl + 1)
        self.c.r["BC"] = bc
        if bc and (not (r[1] & 0x40)):
            self.c.r["PC"] = word(self.c.r["PC"] - 2)
        return "CPI"

    def cpd(self):
        bc = word(self.c.r["BC"] - 1)
        hl = self.c.r["HL"]
        r = sub8(self.c.r["A"], self.c.rdmem(hl), 0)
        t = r[0] - ((r[1] & 0x10) >> 4)
        f = 0x02 | (0x04 if bc else 0)
        f |= (t & 0x08) | ((t & 0x02) >> 4) | self.c.r.flag["C"]
        self.c.r["F"] = (r[1] & 0xD0) | f
        self.c.r["HL"] = word(hl - 1)
        self.c.r["BC"] = bc
        return "CPD"

    def cpdr(self):
        bc = word(self.c.r["BC"] - 1)
        hl = self.c.r["HL"]
        r = sub8(self.c.r["A"], self.c.rdmem(hl), 0)
        t = r[0] - ((r[1] & 0x10) >> 4)
        f = 0x02 | (0x04 if bc else 0)
        f |= (t & 0x08) | ((t & 0x02) >> 4) | self.c.r.flag["C"]
        self.c.r["F"] = (r[1] & 0xD0) | f
        self.c.r["HL"] = word(hl - 1)
        self.c.r["BC"] = bc
        if bc and (not (r[1] & 0x40)):
            self.c.r["PC"] = word(self.c.r["PC"] - 2)
        return "CPDR"
        return

    def ini(self):
        r = sub8(self.c.r["B"], 1, 0)
        hl = self.c.r["HL"]
        self.c.wrmem(hl, self.c.rdinp(self.c.r["BC"]))
        self.c.r["HL"] = word(hl + 1)
        self.c.r["B"] = r[0]
        self.c.r["F"] = self.c.r.flag["C"] | (r[1] & 0xFE)
        return "INI"

    def inir(self):
        r = sub8(self.c.r["B"], 1, 0)
        hl = self.c.r["HL"]
        self.c.wrmem(hl, self.c.rdinp(self.c.r["BC"]))
        self.c.r["HL"] = word(hl + 1)
        self.c.r["B"] = r[0]
        self.c.r["F"] = self.c.r.flag["C"] | (r[1] & 0xFE)
        if not r[0]:
            self.c.r["PC"] = word(self.c.r["PC"] - 2)
        return "INIR"

    def ind(self):
        r = sub8(self.c.r["B"], 1, 0)
        hl = self.c.r["HL"]
        self.c.wrmem(hl, self.c.rdinp(self.c.r["BC"]))
        self.c.r["HL"] = word(hl - 1)
        self.c.r["B"] = r[0]
        self.c.r["F"] = self.c.r.flag["C"] | (r[1] & 0xFE)
        return "IND"

    def indr(self):
        r = sub8(self.c.r["B"], 1, 0)
        hl = self.c.r["HL"]
        self.c.wrmem(hl, self.c.rdinp(self.c.r["BC"]))
        self.c.r["HL"] = word(hl + 1)
        self.c.r["B"] = r[0]
        self.c.r["F"] = self.c.r.flag["C"] | (r[1] & 0xFE)
        if not r[0]:
            self.c.r["PC"] = word(self.c.r["PC"] - 2)
        return "INDR"

    def outi(self):
        r = sub8(self.c.r["B"], 1, 0)
        hl = self.c.r["HL"]
        self.c.wrout(self.c.r["BC"], self.c.rdmem(hl))
        self.c.r["HL"] = word(hl + 1)
        self.c.r["B"] = r[0]
        self.c.r["F"] = self.c.r.flag["C"] | (r[1] & 0xFE)
        return "OUTI"

    def otir(self):
        r = sub8(self.c.r["B"], 1, 0)
        hl = self.c.r["HL"]
        self.c.wrout(self.c.r["BC"], self.c.rdmem(hl))
        self.c.r["HL"] = word(hl + 1)
        self.c.r["B"] = r[0]
        self.c.r["F"] = self.c.r.flag["C"] | (r[1] & 0xFE)
        if not r[0]:
            self.c.r["PC"] = word(self.c.r["PC"] - 2)
        return "OTIR"

    def outd(self):
        r = sub8(self.c.r["B"], 1, 0)
        hl = self.c.r["HL"]
        self.c.wrout(self.c.r["BC"], self.c.rdmem(hl))
        self.c.r["HL"] = word(hl - 1)
        self.c.r["B"] = r[0]
        self.c.r["F"] = self.c.r.flag["C"] | (r[1] & 0xFE)
        return "OUTD"

    def otdr(self):
        r = sub8(self.c.r["B"], 1, 0)
        hl = self.c.r["HL"]
        self.c.wrout(self.c.r["BC"], self.c.rdmem(hl))
        self.c.r["HL"] = word(hl - 1)
        self.c.r["B"] = r[0]
        self.c.r["F"] = self.c.r.flag["C"] | (r[1] & 0xFE)
        if not r[0]:
            self.c.r["PC"] = word(self.c.r["PC"] - 2)
        return "OTDR"

    def getinstr(self):
        rv = {}

        # ldi, ldir, ldd, lddr
        # cpi, cpir, cpd, cpdr
        rv.update({bytes([0xED, 0xA0]): self.ldi})
        rv.update({bytes([0xED, 0xB0]): self.ldir})
        rv.update({bytes([0xED, 0xA8]): self.ldd})
        rv.update({bytes([0xED, 0xB8]): self.lddr})
        rv.update({bytes([0xED, 0xA1]): self.cpi})
        rv.update({bytes([0xED, 0xB1]): self.cpir})
        rv.update({bytes([0xED, 0xA9]): self.cpd})
        rv.update({bytes([0xED, 0xB9]): self.cpdr})

        # ini, inir, ind, indr
        # outi, otir, outd, otdr
        rv.update({bytes([0xED, 0xA2]): self.ini})
        rv.update({bytes([0xED, 0xB2]): self.inir})
        rv.update({bytes([0xED, 0xAA]): self.ind})
        rv.update({bytes([0xED, 0xBA]): self.indr})
        rv.update({bytes([0xED, 0xA3]): self.outi})
        rv.update({bytes([0xED, 0xB3]): self.otir})
        rv.update({bytes([0xED, 0xAB]): self.outd})
        rv.update({bytes([0xED, 0xBB]): self.otdr})

        return rv
