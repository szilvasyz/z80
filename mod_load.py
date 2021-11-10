#
# Z80 load and exchange instructions
#


from utils import *


class load:

    def __init__(self, parent):
        self.c = parent

    def loadrr(self):
        r0s = rname[self.c.r0]
        r1s = rname[self.c.r1]
        self.c.r[r0s] = self.c.r[r1s]
        return "LD {:s},{:s}".format(r0s, r1s)

    def loadxx(self):
        r0s = rxname[self.c.r0]
        r1s = rxname[self.c.r1]
        self.c.r[r0s] = self.c.r[r1s]
        return "LD {:s},{:s}".format(r0s, r1s)

    def loadyy(self):
        r0s = ryname[self.c.r0]
        r1s = ryname[self.c.r1]
        self.c.r[r0s] = self.c.r[r1s]
        return "LD {:s},{:s}".format(r0s, r1s)

    def loadrm(self):
        r0s = rname[self.c.r0]
        d = self.c.rdmem(self.c.r["HL"])
        self.c.r[r0s] = d
        return "LD {:s},(HL)".format(r0s)

    def loadmr(self):
        r1s = rname[self.c.r1]
        d = self.c.r[r1s]
        self.c.wrmem(self.c.r["HL"], d)
        return "LD (HL),{:s}".format(r1s)

    def loadrxm(self):
        dsp = self.c.fetch()
        r0s = rname[self.c.r0]
        d = self.c.rdmem(adddsp(self.c.r["IX"], dsp))
        self.c.r[r0s] = d
        return "LD {:s},(IX+{:02x})".format(r0s, dsp)

    def loadxmr(self):
        dsp = self.c.fetch()
        r1s = rname[self.c.r1]
        d = self.c.r[r1s]
        self.c.wrmem(adddsp(self.c.r["IX"], dsp), d)
        return "LD (IX+{:02x}),{:s}".format(dsp, r1s)

    def loadrym(self):
        dsp = self.c.fetch()
        r0s = rname[self.c.r0]
        d = self.c.rdmem(adddsp(self.c.r["IY"], dsp))
        self.c.r[r0s] = d
        return "LD {:s},(IY+{:02x})".format(r0s, dsp)

    def loadymr(self):
        dsp = self.c.fetch()
        r1s = rname[self.c.r1]
        d = self.c.r[r1s]
        self.c.wrmem(adddsp(self.c.r["IY"], dsp), d)
        return "LD (IY+{:02x}),{:s}".format(dsp, r1s)

    def loadri(self):
        d = self.c.fetch()
        r0s = rname[self.c.r0]
        self.c.r[r0s] = d
        return "LD {:s},{:02X}".format(r0s, d)

    def loadrxi(self):
        d = self.c.fetch()
        r0s = rxname[self.c.r0]
        self.c.r[r0s] = d
        return "LD {:s},{:02X}".format(r0s, d)

    def loadryi(self):
        d = self.c.fetch()
        r0s = ryname[self.c.r0]
        self.c.r[r0s] = d
        return "LD {:s},{:02X}".format(r0s, d)

    def loadmi(self):
        d = self.c.fetch()
        self.c.wrmem(self.c.r["HL"], d)
        return "LD (HL),{:02X}".format(d)

    def loadxmi(self):
        dsp = self.c.fetch()
        d = self.c.fetch()
        a = adddsp(self.c.r["IX"], dsp)
        self.c.wrmem(a, d)
        return "LD (IX+{:02X}),{:02X}".format(dsp, d)

    def loadymi(self):
        dsp = self.c.fetch()
        d = self.c.fetch()
        a = adddsp(self.c.r["IY"], dsp)
        self.c.wrmem(a, d)
        return "LD (IY+{:02X}),{:02X}".format(dsp, d)

    def loadrpi(self):
        rps = rpname[self.c.rp]
        d = self.c.fetch16()
        self.c.r[rps] = d
        return "LD {:s},{:04X}".format(rps, d)

    def loadrpxi(self):
        rps = rpxname[self.c.rp]
        d = self.c.fetch16()
        self.c.r[rps] = d
        return "LD {:s},{:04X}".format(rps, d)

    def loadrpyi(self):
        rps = rpyname[self.c.rp]
        d = self.c.fetch16()
        self.c.r[rps] = d
        return "LD {:s},{:04X}".format(rps, d)

    def loadrpa(self):
        rps = rpname[self.c.rp]
        self.c.wrmem(self.c.r[rps], self.c.r["A"])
        return "LD ({:s}),A".format(rps)

    def loadarp(self):
        rps = rpname[self.c.rp]
        self.c.r["A"] = self.c.rdmem(self.c.r[rps])
        return "LD A,({:s})".format(rps)

    def loadna(self):
        a = self.c.fetch16()
        self.c.wrmem(a, self.c.r["A"])
        return "LD ({:04X}),A".format(a)

    def loadan(self):
        a = self.c.fetch16()
        self.c.r["A"] = self.c.rdmem(a)
        return "LD A,({:04X})".format(a)

    def loadnrp(self):
        rps = rpname[self.c.rp]
        a = self.c.fetch16()
        self.c.wrmem16(a, self.c.r[rps])
        return "LD ({:04X}),{:s}".format(a, rps)

    def loadrpn(self):
        rps = rpname[self.c.rp]
        a = self.c.fetch16()
        self.c.r[rps] = self.c.rdmem16(a)
        return "LD {:s},({:04X})".format(rps, a)

    def loadnrpx(self):
        rps = rpxname[self.c.rp]
        a = self.c.fetch16()
        self.c.wrmem16(a, self.c.r[rps])
        return "LD ({:04X}),{:s}".format(a, rps)

    def loadrpxn(self):
        rps = rpxname[self.c.rp]
        a = self.c.fetch16()
        self.c.r[rps] = self.c.rdmem16(a)
        return "LD {:s},({:04X})".format(rps, a)

    def loadnrpy(self):
        rps = rpyname[self.c.rp]
        a = self.c.fetch16()
        self.c.wrmem16(a, self.c.r[rps])
        return "LD ({:04X}),{:s}".format(a, rps)

    def loadrpyn(self):
        rps = rpyname[self.c.rp]
        a = self.c.fetch16()
        self.c.r[rps] = self.c.rdmem16(a)
        return "LD {:s},({:04X})".format(rps, a)

    def loadsphl(self):
        self.c.r["SP"] = self.c.r["HL"]
        return "LD SP,HL"

    def loadspix(self):
        self.c.r["SP"] = self.c.r["IX"]
        return "LD SP,IX"

    def loadspiy(self):
        self.c.r["SP"] = self.c.r["IY"]
        return "LD SP,IY"

    def ldia(self):
        self.c.r["I"] = self.c.r["A"]
        return "LD I,A"

    def ldai(self):
        d = self.c.r["I"]
        i = self.c.iff2
        self.c.r["A"] = d
        self.c.r["F"] = (logf(d) & 0xfa) | self.c.r.flag["C"] | (i << 2)
        return "LD A,I"

    def ldra(self):
        self.c.r["R"] = self.c.r["A"]
        return "LD R,A"

    def ldar(self):
        d = self.c.r["R"]
        i = self.c.iff2
        self.c.r["A"] = d
        self.c.r["F"] = (logf(d) & 0xfa) | self.c.r.flag["C"] | (i << 2)
        return "LD A,R"

    def exa(self):
        self.c.r.exa()
        return "EX AF,AF'"

    def exx(self):
        self.c.r.exx()
        return "EXX"

    def exdehl(self):
        d = self.c.r["DE"]
        self.c.r["DE"] = self.c.r["HL"]
        self.c.r["HL"] = d
        return "EX DE,HL"

    def exsphl(self):
        a = self.c.r["SP"]
        d = self.c.rdmem(a)
        self.c.wrmem(a, self.c.r["HL"])
        self.c.r["HL"] = d
        return "EX (SP),HL"

    def exspix(self):
        a = self.c.r["SP"]
        d = self.c.rdmem(a)
        self.c.wrmem(a, self.c.r["IX"])
        self.c.r["IX"] = d
        return "EX (SP),IX"

    def exspiy(self):
        a = self.c.r["SP"]
        d = self.c.rdmem(a)
        self.c.wrmem(a, self.c.r["IY"])
        self.c.r["IY"] = d
        return "EX (SP),IY"

    def getinstr(self):
        rv = {}

        # load r, r
        for r0 in [0, 1, 2, 3, 4, 5, 7]:
            for r1 in [0, 1, 2, 3, 4, 5, 7]:
                rv.update({bytes([0x40 | (r0 << 3) | r1]): self.loadrr})
                rv.update({bytes([0xdd, 0x40 | (r0 << 3) | r1]): self.loadxx})
                rv.update({bytes([0xfd, 0x40 | (r0 << 3) | r1]): self.loadyy})

        # load r,m; load m,r; load r,imm
        for r0 in [0, 1, 2, 3, 4, 5, 7]:
            rv.update({bytes([0x46 | (r0 << 3)]): self.loadrm})
            rv.update({bytes([0xdd, 0x46 | (r0 << 3)]): self.loadrxm})
            rv.update({bytes([0xfd, 0x46 | (r0 << 3)]): self.loadrym})
            rv.update({bytes([0x70 | r0]): self.loadmr})
            rv.update({bytes([0xdd, 0x70 | r0]): self.loadxmr})
            rv.update({bytes([0xfd, 0x70 | r0]): self.loadymr})
            rv.update({bytes([0x6 | (r0 << 3)]): self.loadri})
            rv.update({bytes([0xdd, 0x6 | (r0 << 3)]): self.loadrxi})
            rv.update({bytes([0xfd, 0x6 | (r0 << 3)]): self.loadryi})

        # load m,imm; load xm,imm; load ym,imm
        rv.update({bytes([0x36]): self.loadmi})
        rv.update({bytes([0xdd, 0x36]): self.loadxmi})
        rv.update({bytes([0xfd, 0x36]): self.loadymi})

        # load rp,imm
        for rp in range(4):
            rv.update({bytes([0x01 | (rp << 4)]): self.loadrpi})
            rv.update({bytes([0xDD, 0x01 | (rp << 4)]): self.loadrpxi})
            rv.update({bytes([0xFD, 0x01 | (rp << 4)]): self.loadrpyi})

        # load (rp),a; load a,(rp)
        for rp in range(2):
            rv.update({bytes([0x02 | (rp << 4)]): self.loadrpa})
            rv.update({bytes([0xDD, 0x02 | (rp << 4)]): self.loadrpa})
            rv.update({bytes([0xFD, 0x02 | (rp << 4)]): self.loadrpa})
            rv.update({bytes([0x0A | (rp << 4)]): self.loadarp})
            rv.update({bytes([0xDD, 0x0A | (rp << 4)]): self.loadarp})
            rv.update({bytes([0xFD, 0x0A | (rp << 4)]): self.loadarp})

        # load (ind),a; load a,(ind)
        rv.update({bytes([0x32]): self.loadna})
        rv.update({bytes([0xDD, 0x32]): self.loadna})
        rv.update({bytes([0xFD, 0x32]): self.loadna})
        rv.update({bytes([0x3A]): self.loadan})
        rv.update({bytes([0xDD, 0x3A]): self.loadan})
        rv.update({bytes([0xFD, 0x3A]): self.loadan})

        # load (ind),hl; load hl,(ind)
        rv.update({bytes([0x22]): self.loadnrp})
        rv.update({bytes([0x2A]): self.loadrpn})
        rv.update({bytes([0xDD, 0x22]): self.loadnrpx})
        rv.update({bytes([0xDD, 0x2A]): self.loadrpxn})
        rv.update({bytes([0xFD, 0x22]): self.loadnrpy})
        rv.update({bytes([0xFD, 0x2A]): self.loadrpyn})

        # load (ind),rp; load rp,(ind)
        for rp in range(4):
            rv.update({bytes([0xED, 0x43 | (rp << 4)]): self.loadnrp})
            rv.update({bytes([0xED, 0x4B | (rp << 4)]): self.loadrpn})

        rv.update({bytes([0xF9]): self.loadsphl})
        rv.update({bytes([0xDD, 0xF9]): self.loadspix})
        rv.update({bytes([0xFD, 0xF9]): self.loadspiy})

        rv.update({bytes([0xED, 0x47]): self.ldia})
        rv.update({bytes([0xED, 0x57]): self.ldai})
        rv.update({bytes([0xED, 0x4F]): self.ldra})
        rv.update({bytes([0xED, 0x5F]): self.ldar})

        rv.update({bytes([0x08]): self.exa})
        rv.update({bytes([0xDD, 0x08]): self.exa})
        rv.update({bytes([0xFD, 0x08]): self.exa})
        rv.update({bytes([0xD9]): self.exx})
        rv.update({bytes([0xDD, 0xD9]): self.exx})
        rv.update({bytes([0xFD, 0xD9]): self.exx})
        rv.update({bytes([0xEB]): self.exdehl})
        rv.update({bytes([0xDD, 0xEB]): self.exdehl})
        rv.update({bytes([0xFD, 0xEB]): self.exdehl})

        rv.update({bytes([0xE3]): self.exsphl})
        rv.update({bytes([0xDD, 0xE3]): self.exspix})
        rv.update({bytes([0xFD, 0xE3]): self.exspiy})

        return rv
