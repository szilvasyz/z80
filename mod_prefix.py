#
# Z80 instruction prefixes and control instructions
#


class prefix:

    def __init__(self, parent):
        self.c = parent

    def nop(self):
        return "NOP"

    def halt(self):
        self.c.halted = True
        return "HALT"

    def di(self):
        self.c.iff1 = 0
        self.c.iff2 = 0
        return "DI"

    def ei(self):
        self.c.iff1 = 1
        self.c.iff2 = 1
        return "EI"

    def scf(self):
        f = self.c.r["F"] & 0xC4 | 1
        f |= self.c.r["A"] & 0x28
        self.c.r["F"] = f
        return "SCF"

    def ccf(self):
        f = self.c.r["F"] & 0xC5
        f |= self.c.r["A"] & 0x28
        f |= (f & 1) << 4
        self.c.r["F"] = f ^ 1
        return "CCF"

    def im0(self):
        self.c.im = 0
        return "IM 0"

    def im1(self):
        self.c.im = 1
        return "IM 1"

    def im2(self):
        self.c.im = 2
        return "IM 2"

    def next(self):
        self.c.next = True
        return ""

    def drop(self):
        self.c.opc = self.c.opc[1:]
        self.c.next = True
        return ""

    def ddcb(self):
        self.c.dsp = self.c.fetch()
        self.c.next = True
        return ""

    def fdcb(self):
        self.c.dsp = self.c.fetch()
        self.c.next = True
        return ""

    def getinstr(self):
        rv = {
            # NOP instruction
            b'\x00': self.nop,
            b'\xdd\x00': self.nop,
            b'\xfd\x00': self.nop,

            # HALT instruction
            b'\x76': self.halt,
            b'\xdd\x76': self.halt,
            b'\xfd\x76': self.halt,

            # set/complement carry flag
            b'\x37': self.scf,
            b'\xdd\x37': self.scf,
            b'\xfd\x37': self.scf,
            b'\x3f': self.ccf,
            b'\xdd\x3f': self.ccf,
            b'\xfd\x3f': self.ccf,

            # enable/disable interrupts
            b'\xf3': self.di,
            b'\xdd\xf3': self.di,
            b'\xfd\xf3': self.di,
            b'\xfb': self.ei,
            b'\xdd\xfb': self.ei,
            b'\xfd\xfb': self.ei,

            # set interrupt modes
            b'\xed\x46': self.im0,
            b'\xed\x56': self.im1,
            b'\xed\x66': self.im0,
            b'\xed\x76': self.im1,
            b'\xed\x4e': self.im0,
            b'\xed\x5e': self.im2,
            b'\xed\x6e': self.im0,
            b'\xed\x7e': self.im2,

            # prefixes
            b'\xdd': self.next, b'\xfd': self.next,
            b'\xcb': self.next, b'\xed': self.next,
            b'\xdd\xdd': self.drop,
            b'\xdd\xed': self.drop,
            b'\xdd\xfd': self.drop,
            b'\xed\xdd': self.drop,
            b'\xed\xed': self.drop,
            b'\xed\xfd': self.drop,
            b'\xfd\xdd': self.drop,
            b'\xfd\xed': self.drop,
            b'\xfd\xfd': self.drop,
            b'\xdd\xcb': self.ddcb,
            b'\xfd\xcb': self.fdcb
        }

        # extended instruction table
        rv.update({bytes([0xED, 0x77]): self.nop})
        rv.update({bytes([0xED, 0x7F]): self.nop})

        for c in list(range(0x00, 0x40)) + list(range(0x80, 0xA0)) + list(range(0xC0, 0x100)):
            rv.update({bytes([0xED, c]): self.nop})

        for c in list(range(0x04, 0x08)) + list(range(0x0c, 0x10)):
            rv.update({bytes([0xED, 0xA0 + c]): self.nop})
            rv.update({bytes([0xED, 0xB0 + c]): self.nop})

        return rv
