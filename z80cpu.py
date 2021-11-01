def signdisp(d):
    if d > 127:
        d = d - 256
    return d

def lobyte(i):
    return i & 0xFF


def hibyte(i):
    return (i >> 8) & 0xff


def inc8(i):
    return (i + 1) & 0xFF


def dec8(i):
    return (i - 1) & 0xFF


def inc16(i):
    return (i + 1) & 0xFFFF


def dec16(i):
    return (i - 1) & 0xFFFF


class regs():
    flags = {"S": 0b10000000, "Z": 0b01000000, "F5": 0b00100000, "H": 0b00010000,
             "F3": 0b00001000, "P": 0b00000100, "N": 0b00000010, "C": 0b00000001}
    regs = {'B': 0, 'C': 0,
            'D': 0, 'E': 0,
            'H': 0, 'L': 0,
            'A': 0, 'F': 0,
            'I': 0, 'R': 0,
            "B'": 0, "C'": 0,
            "D'": 0, "E'": 0,
            "H'": 0, "L'": 0,
            "A'": 0, "F'": 0,
            'XH': 0, 'XL': 0,
            'YH': 0, 'YL': 0,
            'SP': 0, 'PC': 0}

    def __setitem__(self, reg, value):

        if reg in ["PC", "SP"]:
            self.regs[reg] = value & 0xFFFF
            return

        if reg in ["BC", "DE", "HL", "AF"]:
            self.regs[reg[0]] = hibyte(value)
            self.regs[reg[1]] = lobyte(value)
            return

        if reg in ["IX", "IY"]:
            self.regs[reg[1] + "H"] = hibyte(value)
            self.regs[reg[1] + "L"] = lobyte(value)
            return

        self.regs[reg] = lobyte(value)

    def __getitem__(self, reg):
        if reg in ["BC", "DE", "HL", "AF"]:
            return (self.regs[reg[0]] << 8) | self.regs[reg[1]]

        if reg in ["IX", "IY"]:
            return (self.regs[reg[1] + "H"] << 8) | self.regs[reg[1] + "L"]

        return self.regs[reg]

    def __str__(self):
        s = "_BC_ _DE_ _HL_ _AF_ _IX_ _IY_ _PC_ _SP_ _I_ _R_\n" \
            "{:04X} {:04X} {:04X} {:04X} {:04X} {:04X} {:04X} {:04X} {:02X} {:02X} "
        return (s.format(
            self["BC"], self["DE"], self["HL"],
            self["AF"], self["IX"], self["IY"],
            self["PC"], self["SP"], self["I"], self["R"])
        )

    def setflag(self, flag, value):
        b = (1 << flag) if type(flag) is int else self.flags[flag]
        if value:
            self.regs["F"] = self.regs["F"] | b
        else:
            self.regs["F"] = self.regs["F"] & (~ b)
        return

    def getflag(self, flag):
        b = (1 << flag) if type(flag) is int else self.flags[flag]
        return 1 if self.regs["F"] & b else 0

    def exa(self):
        t = self["A"]; self["A"] = self["A'"]; self["A'"] = t
        t = self["F"]; self["F"] = self["F'"]; self["F'"] = t
        return

    def exx(self):
        t = self["B"]; self["B"] = self["B'"]; self["B'"] = t
        t = self["C"]; self["C"] = self["C'"]; self["C'"] = t
        t = self["D"]; self["D"] = self["D'"]; self["D'"] = t
        t = self["E"]; self["E"] = self["E'"]; self["E'"] = t
        t = self["H"]; self["H"] = self["H'"]; self["H'"] = t
        t = self["L"]; self["L"] = self["L'"]; self["L'"] = t
        return


#
# Instruction executing constants
#


rname = ["B", "C", "D", "E", "H", "L", "M", "A"]
rpname = ["BC", "DE", "HL", "SP"]
rp2name = ["BC", "DE", "HL", "AF"]


#
# Instruction executing functions
#

#
# - generic -
#
def noop(obj):
    return


def halt(obj):
    obj.halted = True
    return


def extd(obj):
    obj.ifprf = True
    obj.prf = "E"
    return


def prix(obj):
    obj.ifprf = True
    obj.prf = "X"
    return


def priy(obj):
    obj.ifprf = True
    obj.prf = "Y"
    return


def bits(obj):
    if obj.prf in ["X", "Y"]:
        obj.dsp = obj.fetch()
        obj.hasdsp = True

    obj.ifprf = True
    obj.prf = "C"
    return


def ei__(obj):
    obj.iff1 = 1
    obj.iff2 = 1
    return


def di__(obj):
    obj.iff1 = 0
    obj.iff2 = 0
    return


def inn_(obj):
    obj.r["A"] = 0xFF
    return


def outn(obj):
    return

#
# - exchanges -
#


def exa_(obj):
    obj.r.exa()
    return


def exx_(obj):
    obj.r.exx()
    return


def exde(obj):
    d = obj.r["DE"]
    obj.r["DE"] = obj.r["HL"]
    obj.r["HL"] = d
    return


def exsp(obj):
    a = obj.r["SP"]
    d = obj.rdmem16(a)
    obj.wrmem16(a, obj.r["HL"])
    obj.r["HL"] = d
    return

#
# - loads -
#


def ldrr(obj):
    obj.r[rname[obj.r0]] = obj.r[rname[obj.r1]]
    return


def ldrm(obj):
    obj.r[rname[obj.r0]] = obj.rdmem(obj.r["HL"])
    return


def ldmr(obj):
    obj.wrmem(obj.r["HL"], obj.r[rname[obj.r1]])
    return


def ldri(obj):
    obj.r[rname[obj.r0]] = obj.fetch()
    return


def ldmi(obj):
    obj.wrmem(obj.r["HL"], obj.fetch())
    return


def ldan(obj):
    obj.r["A"] = obj.rdmem(obj.fetch16())
    return


def ldna(obj):
    obj.wrmem(obj.fetch16(), obj.r["A"])
    return


def ldap(obj):
    obj.r["A"] = obj.rdmem(obj.r[rpname[obj.rp]])
    return


def ldpa(obj):
    obj.wrmem(obj.r[rpname[obj.rp]], obj.r["A"])
    return


def ldpn(obj):
    a = obj.fetch16()
    obj.r[rpname[obj.rp]] = obj.rdmem(a) | (obj.rdmem(inc16(a)))
    return


def ldnp(obj):
    a = obj.fetch16()
    obj.wrmem(a, lobyte(obj.r[rpname[obj.rp]]))
    obj.wrmem(inc16(a), hibyte(obj.r[rpname[obj.rp]]))
    return


def ldpi(obj):
    a = obj.fetch16()
    obj.r[rpname[obj.rp]] = a
    return


def ldsp(obj):
    obj.r["SP"] = obj.r["HL"]
    return

#
# - inc/dec -
#


def incp(obj):
    obj.r[rpname[obj.rp]] = inc16(obj.r[rpname[obj.rp]])
    return


def decp(obj):
    obj.r[rpname[obj.rp]] = dec16(obj.r[rpname[obj.rp]])
    return


def incr(obj):
    obj.r[rname[obj.r1]] = inc8(obj.r[rname[obj.r1]])
    return


def incm(obj):
    a = obj.r["HL"]
    obj.wrmem(a, inc8(obj.rdmem(a)))
    return


def decr(obj):
    obj.r[rname[obj.r1]] = inc8(obj.r[rname[obj.r1]])
    return


def decm(obj):
    a = obj.r["HL"]
    obj.wrmem(a, inc8(obj.rdmem(a)))
    return


#
# - add/sub -
#


def addp(obj):
    d = obj.r[rpname[obj.rp]]
    obj.r["HL"] = (obj.r["HL"] + d) & 0xFFFF
    return


def adcp(obj):
    d = obj.r[rpname[obj.rp]]
    obj.r["HL"] = (obj.r["HL"] + d + obj.r.getflag("C")) & 0xFFFF
    return


def addr(obj):
    d = obj.r[rname[obj.r1]]
    obj.r["A"] = (obj.r["A"] + d) & 0xFF
    return


def addm(obj):
    d = obj.rdmem(obj.r["HL"])
    obj.r["A"] = (obj.r["A"] + d) & 0xFF
    return


def addi(obj):
    d = obj.fetch()
    obj.r["A"] = (obj.r["A"] + d) & 0xFF
    return


def adcr(obj):
    d = obj.r[rname[obj.r1]]
    obj.r["A"] = (obj.r["A"] + d + obj.r.getflag("C")) & 0xFF
    return


def adcm(obj):
    d = obj.rdmem(obj.r["HL"])
    obj.r["A"] = (obj.r["A"] + d + obj.r.getflag("C")) & 0xFF
    return


def adci(obj):
    d = obj.fetch()
    obj.r["A"] = (obj.r["A"] + d + obj.r.getflag("C")) & 0xFF
    return


def sbcp(obj):
    d = obj.r[rpname[obj.rp]]
    obj.r["HL"] = (obj.r["HL"] - d - obj.r.getflag("C")) & 0xFFFF
    return


def subr(obj):
    d = obj.r[rname[obj.r1]]
    obj.r["A"] = (obj.r["A"] - d) & 0xFF
    return


def subm(obj):
    d = obj.rdmem(obj.r["HL"])
    obj.r["A"] = (obj.r["A"] - d) & 0xFF
    return


def subi(obj):
    d = obj.fetch()
    obj.r["A"] = (obj.r["A"] - d) & 0xFF
    return


def sbcr(obj):
    d = obj.r[rname[obj.r1]]
    obj.r["A"] = (obj.r["A"] - d - obj.r.getflag("C")) & 0xFF
    return


def sbcm(obj):
    d = obj.rdmem(obj.r["HL"])
    obj.r["A"] = (obj.r["A"] - d - obj.r.getflag("C")) & 0xFF
    return


def sbci(obj):
    d = obj.fetch()
    obj.r["A"] = (obj.r["A"] - d - obj.r.getflag("C")) & 0xFF
    return

#
# - and/or/xor/cp -
#


def andr(obj):
    d = obj.r[rname[obj.r1]]
    obj.r["A"] = (obj.r["A"] & d)
    return


def andm(obj):
    d = obj.rdmem(obj.r["HL"])
    obj.r["A"] = (obj.r["A"] & d)
    return


def andi(obj):
    d = obj.fetch()
    obj.r["A"] = (obj.r["A"] & d)
    return


def orr_(obj):
    d = obj.r[rname[obj.r1]]
    obj.r["A"] = (obj.r["A"] | d)
    return


def orm_(obj):
    d = obj.rdmem(obj.r["HL"])
    obj.r["A"] = (obj.r["A"] | d)
    return


def ori_(obj):
    d = obj.fetch()
    obj.r["A"] = (obj.r["A"] | d)
    return


def xorr(obj):
    d = obj.r[rname[obj.r1]]
    obj.r["A"] = (obj.r["A"] ^ d)
    return


def xorm(obj):
    d = obj.rdmem(obj.r["HL"])
    obj.r["A"] = (obj.r["A"] ^ d)
    return


def xori(obj):
    d = obj.fetch()
    obj.r["A"] = (obj.r["A"] ^ d)
    return


def cpr_(obj):
    d = obj.r["A"] - obj.r[rname[obj.r1]]
    return


def cpm_(obj):
    d = obj.r["A"] - obj.rdmem(obj.r["HL"])
    return


def cpi_(obj):
    d = obj.r["A"] - obj.fetch()
    return

#
# - rots -
#


def rlca(obj):
    d = obj.r["A"]
    c = (d >> 7) & 0x01
    obj.r["A"] = ((d << 1) | c) & 0xFF
    obj.r.setflag("C", c)
    return


def rla_(obj):
    d = obj.r["A"]
    c = (d >> 7) & 0x01
    obj.r["A"] = ((d << 1) | obj.r.getflag("C")) & 0xFF
    obj.r.setflag("C", c)
    return


def rrca(obj):
    d = obj.r["A"]
    c = d & 0x01
    obj.r["A"] = ((d >> 1) | (c << 7)) & 0xFF
    obj.r.setflag("C", c)
    return


def rra_(obj):
    d = obj.r["A"]
    c = d & 0x01
    obj.r["A"] = ((d >> 1) | (obj.r.getflag("C") << 7)) & 0xFF
    obj.r.setflag("C", c)
    return


def daa_(obj):
    return


def cpla(obj):
    obj.r["A"] = (~ obj.r["A"]) & 0xFF
    return


def setc(obj):
    obj.r.setflag("C", 1)
    return


def cplc(obj):
    obj.r.setflag("C", 1 - obj.r.getflag("C"))
    return

#
# - branches -
#


def djnz(obj):
    d = signdisp(obj.fetch())
    b = (obj.r["B"] - 1) & 0xFF
    obj.r["B"] = b
    if b != 0:
        obj.r["PC"] = (obj.r["PC"] + d) & 0xFFFF
    return


def jrnz(obj):
    d = signdisp(obj.fetch())
    if not obj.r.getflag("Z"):
        obj.r["PC"] = (obj.r["PC"] + d) & 0xFFFF
    return


def jrnc(obj):
    d = signdisp(obj.fetch())
    if not obj.r.getflag("C"):
        obj.r["PC"] = (obj.r["PC"] + d) & 0xFFFF
    return


def jr__(obj):
    d = signdisp(obj.fetch())
    obj.r["PC"] = (obj.r["PC"] + d) & 0xFFFF
    return


def jrz_(obj):
    d = signdisp(obj.fetch())
    if obj.r.getflag("Z"):
        obj.r["PC"] = (obj.r["PC"] + d) & 0xFFFF
    return


def jrc_(obj):
    d = signdisp(obj.fetch())
    if obj.r.getflag("C"):
        obj.r["PC"] = (obj.r["PC"] + d) & 0xFFFF
    return

#
# - jumps -
#


def jp__(obj):
    a = obj.fetch16()
    obj.r["PC"] = a
    return


def jpnz(obj):
    a = obj.fetch16()
    if not obj.r.getflag("Z"):
        obj.r["PC"] = a
    return


def jpz_(obj):
    a = obj.fetch16()
    if obj.r.getflag("Z"):
        obj.r["PC"] = a
    return


def jpnc(obj):
    a = obj.fetch16()
    if not obj.r.getflag("C"):
        obj.r["PC"] = a
    return


def jpc_(obj):
    a = obj.fetch16()
    if obj.r.getflag("C"):
        obj.r["PC"] = a
    return


def jppo(obj):
    a = obj.fetch16()
    if not obj.r.getflag("P"):
        obj.r["PC"] = a
    return


def jppe(obj):
    a = obj.fetch16()
    if obj.r.getflag("P"):
        obj.r["PC"] = a
    return


def jpp_(obj):
    a = obj.fetch16()
    if not obj.r.getflag("S"):
        obj.r["PC"] = a
    return


def jpm_(obj):
    a = obj.fetch16()
    if obj.r.getflag("S"):
        obj.r["PC"] = a
    return


def jphl(obj):
    obj.r["PC"] = obj.r["HL"]
    return

#
# - calls -
#
def call(obj):
    a = obj.fetch16()
    obj.push(obj.r["PC"])
    obj.r["PC"] = a
    return


def clnz(obj):
    a = obj.fetch16()
    if not obj.r.getflag("Z"):
        obj.push(obj.r["PC"])
        obj.r["PC"] = a
    return


def clz_(obj):
    a = obj.fetch16()
    if obj.r.getflag("Z"):
        obj.push(obj.r["PC"])
        obj.r["PC"] = a
    return


def clnc(obj):
    a = obj.fetch16()
    if not obj.r.getflag("C"):
        obj.push(obj.r["PC"])
        obj.r["PC"] = a
    return


def clc_(obj):
    a = obj.fetch16()
    if obj.r.getflag("C"):
        obj.push(obj.r["PC"])
        obj.r["PC"] = a
    return


def clpo(obj):
    a = obj.fetch16()
    if not obj.r.getflag("P"):
        obj.push(obj.r["PC"])
        obj.r["PC"] = a
    return


def clpe(obj):
    a = obj.fetch16()
    if obj.r.getflag("P"):
        obj.push(obj.r["PC"])
        obj.r["PC"] = a
    return


def clp_(obj):
    a = obj.fetch16()
    if not obj.r.getflag("S"):
        obj.push(obj.r["PC"])
        obj.r["PC"] = a
    return


def clm_(obj):
    a = obj.fetch16()
    if obj.r.getflag("S"):
        obj.push(obj.r["PC"])
        obj.r["PC"] = a
    return

def rs00(obj):
    obj.push(obj.r["PC"])
    obj.r["PC"] = 0x00
    return

def rs08(obj):
    obj.push(obj.r["PC"])
    obj.r["PC"] = 0x08
    return


def rs10(obj):
    obj.push(obj.r["PC"])
    obj.r["PC"] = 0x10
    return


def rs18(obj):
    obj.push(obj.r["PC"])
    obj.r["PC"] = 0x18
    return


def rs20(obj):
    obj.push(obj.r["PC"])
    obj.r["PC"] = 0x20
    return


def rs28(obj):
    obj.push(obj.r["PC"])
    obj.r["PC"] = 0x28
    return


def rs30(obj):
    obj.push(obj.r["PC"])
    obj.r["PC"] = 0x30
    return


def rs38(obj):
    obj.push(obj.r["PC"])
    obj.r["PC"] = 0x38
    return

#
# - rets -
#
def ret_(obj):
    obj.r["PC"] = obj.pop()
    return


def rtnz(obj):
    if not obj.r.getflag("Z"):
        obj.r["PC"] = obj.pop()
    return


def rtz_(obj):
    if obj.r.getflag("Z"):
        obj.r["PC"] = obj.pop()
    return


def rtnc(obj):
    if not obj.r.getflag("C"):
        obj.r["PC"] = obj.pop()
    return


def rtc_(obj):
    if obj.r.getflag("C"):
        obj.r["PC"] = obj.pop()
    return


def rtpo(obj):
    if not obj.r.getflag("P"):
        obj.r["PC"] = obj.pop()
    return


def rtpe(obj):
    if obj.r.getflag("P"):
        obj.r["PC"] = obj.pop()
    return


def rtp_(obj):
    if not obj.r.getflag("S"):
        obj.r["PC"] = obj.pop()
    return


def rtm_(obj):
    if obj.r.getflag("S"):
        obj.r["PC"] = obj.pop()
    return

#
# - pushs/pops -
#


def push(obj):
    obj.push(obj.r[rp2name[obj.rp]])
    return


def pop_(obj):
    obj.r[rp2name[obj.rp]] = obj.pop()
    return


#
#
# CPU main class
#


class cpu():
    r = regs()
    mem = []
    iff1 = 0
    iff2 = 0

    prf = " "
    dsp = 0
    opc = 0
    dta = 0
    hasdsp = False
    halted = False
    ifprf = True
    r0 = 0
    r1 = 0
    rp = 0

    #
    # Instruction tables
    # Instructions:
    #
    # - generic -
    # noop - no operation
    # prix - IX prefix
    # priy - IY prefix
    # extd - ED prefix
    # ei__ - enable interrupts
    # di__ - disable interrupts
    # inn_ - in indirect to A
    # outn - out indirect from A
    #
    # - exchanges -
    # exa_ - exchange AF with A'F'
    # exx_ - exchange CD, DE, HL with B'C', D'E', H'L'
    # exde - exchange DE with HL
    # exsp - exchange (SP) HL
    #
    # - loads -
    # ldrr - load reg from reg
    # ldrm - load reg from M
    # ldmr - load M from reg
    # ldri - load reg from immediate
    # ldmi - load M from immediate
    # ldan - load a from indirect
    # ldna - load indirect from a
    # ldap - load a from (regpair)
    # ldpa - load (regpair) from a
    # ldpn - load regpair from indirect
    # ldnp - load indirect from regpair
    # ldpi - load regpair from immediate
    # ldsp - load SP from HL
    #
    # - inc/dec -
    # incp - increment regpair
    # decp - decrement regpair
    # incr - increment reg
    # incm - increment M
    # decr - decrement reg
    # decm - decrement M
    #
    # - add/sub -
    # addp - add regpair to HL
    # adcp - add regpair to HL with C
    # addr - add reg to A
    # addm - add M to A
    # addi - add immediate to A
    # adcr - add reg to A with C
    # adcm - add M to A with C
    # adci - add immediate to A with C
    #
    # sbcp - sub regpair from HL with C
    # subr - sub reg from A
    # subm - sub M from A
    # subi - sub immediate from A
    # sbcr - sub reg from A with C
    # sbcm - sub M from A with C
    # sbci - sub immediate from A with C
    #
    # - and/or/xor/cp -
    # andr - A and reg
    # andm - A and M
    # andi - A and immediate
    # orr_ - A or reg
    # orm_ - A or M
    # ori_ - A or immediate
    # xorr - A xor reg
    # xorm - A xor M
    # xori - A xor immediate
    # cpr_ - A - reg
    # cpm_ - A - M
    # cpi_ - A - immediate
    #
    # - rots -
    # rlca - rotate A left
    # rla_ - rotate A left through C
    # rrca - rotate A right
    # rra_ - rotate A right through C
    # daa_ - decimal adjust A
    # cpla - complement A
    # setc - set C flag
    # cplc - complement C flag
    #
    # - branches -
    # djnz - decrement B and jump rel if not zero
    # jrnz - jump rel if Z=0
    # jrnc - jump rel if C=0
    # jr__ - jump rel
    # jrz_ - jump rel if Z=1
    # jrc_ - jump rel if C=1
    #
    # - jumps -
    # jp__ - jump
    # jpnz - jump if Z=0
    # jpz_ - jump if Z=1
    # jpnc - jump if C=0
    # jpc_ - jump if C=1
    # jppo - jump if P=0
    # jppe - jump if P=1
    # jpp_ - jump if S=0
    # jpm_ - jump if S=1
    # jphl - jump to HL
    #
    # - calls -
    # call - call
    # clnz - call if Z=0
    # clz_ - call if Z=1
    # clnc - call if C=0
    # clc_ - call if C=1
    # clpo - call if P=0
    # clpe - call if P=1
    # clp_ - call if S=0
    # clm_ - call if S=1
    # rs00 - rst 00
    # rs08 - rst 08
    # rs10 - rst 10
    # rs18 - rst 18
    # rs20 - rst 20
    # rs28 - rst 28
    # rs30 - rst 30
    # rs38 - rst 38
    #
    # - rets -
    # ret_ - return
    # rtnz - return if Z=0
    # rtz_ - return if Z=1
    # rtnc - return if C=0
    # rtc_ - return if C=1
    # rtpo - return if P=0
    # rtpe - return if P=1
    # rtp_ - return if S=0
    # rtm_ - return if S=1
    #
    # - pushs/pops -
    # push - push reg pair2
    # pop_ - pop reg pair2
    #

    instr = {
        " ": [
            noop, ldpi, ldpa, incp, incr, decr, ldri, rlca, exa_, addp, ldap, decp, incr, decr, ldri, rrca,
            djnz, ldpi, ldpa, incp, incr, decr, ldri, rla_, jr__, addp, ldap, decp, incr, decr, ldri, rra_,
            jrnz, ldpi, ldnp, incp, incr, decr, ldri, daa_, jrz_, addp, ldpn, decp, incr, decr, ldri, cpla,
            jrnc, ldpi, ldna, incp, incm, decm, ldmi, setc, jrc_, addp, ldan, decp, incm, decm, ldri, cplc,
            ldrr, ldrr, ldrr, ldrr, ldrr, ldrr, ldrm, ldrr, ldrr, ldrr, ldrr, ldrr, ldrr, ldrr, ldrm, ldrr,
            ldrr, ldrr, ldrr, ldrr, ldrr, ldrr, ldrm, ldrr, ldrr, ldrr, ldrr, ldrr, ldrr, ldrr, ldrm, ldrr,
            ldrr, ldrr, ldrr, ldrr, ldrr, ldrr, ldrm, ldrr, ldrr, ldrr, ldrr, ldrr, ldrr, ldrr, ldrm, ldrr,
            ldmr, ldmr, ldmr, ldmr, ldmr, ldmr, halt, ldmr, ldrr, ldrr, ldrr, ldrr, ldrr, ldrr, ldrm, ldrr,
            addr, addr, addr, addr, addr, addr, addm, addr, adcr, adcr, adcr, adcr, adcr, adcr, adcm, adcr,
            subr, subr, subr, subr, subr, subr, subm, subr, sbcr, sbcr, sbcr, sbcr, sbcr, sbcr, sbcm, sbcr,
            andr, andr, andr, andr, andr, andr, andm, andr, xorr, xorr, xorr, xorr, xorr, xorr, xorm, xorr,
            orr_, orr_, orr_, orr_, orr_, orr_, orm_, orr_, cpr_, cpr_, cpr_, cpr_, cpr_, cpr_, cpm_, cpr_,
            rtnz, pop_, jpnz, jp__, clnz, push, addi, rs00, rtz_, ret_, jpz_, bits, clz_, call, adci, rs08,
            rtnc, pop_, jpnc, outn, clnc, push, subi, rs10, rtc_, exx_, jpc_, inn_, clc_, prix, sbci, rs18,
            rtpo, pop_, jppo, exsp, clpo, push, andi, rs20, rtpe, jphl, jppe, exde, clpe, extd, xori, rs28,
            rtp_, pop_, jpp_, di__, clp_, push, ori_, rs30, rtm_, ldsp, jpm_, ei__, clm_, priy, cpi_, rs38
        ],
        "X": [
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, bits, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, prix, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, extd, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, priy, noop, noop
        ],
        "Y": [
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, bits, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, prix, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, extd, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, priy, noop, noop
        ],
        "E": [
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, ldnp, noop, noop, noop, noop, noop, noop, adcp, ldpn, noop, noop, noop, noop,
            noop, noop, noop, ldnp, noop, noop, noop, noop, noop, noop, adcp, ldpn, noop, noop, noop, noop,
            noop, noop, noop, ldnp, noop, noop, noop, noop, noop, noop, adcp, ldpn, noop, noop, noop, noop,
            noop, noop, noop, ldnp, noop, noop, noop, noop, noop, noop, adcp, ldpn, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, bits, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, prix, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, extd, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, priy, noop, noop
        ],
        "C": [
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop,
            noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop, noop
        ]

    }

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
        a = (self.r["SP"] - 2) & 0xFFFF
        self.wrmem16(a, data)
        self.r["SP"] = a

    def pop(self):
        a = self.r["SP"]
        d = self.rdmem16(a)
        self.r["SP"] = (a + 2) & 0xFFFF
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
        self.prf = " "
        self.dsp = 0
        self.opc = 0
        self.dta = 0
        self.hasdsp = False
        self.ifprf = True

        while self.ifprf:
            b = self.fetch()
            self.r0 = (b >> 3) & 7
            self.r1 = b & 7
            self.rp = (b >> 4) & 3
            self.ifprf = False

            self.instr[self.prf][b](self)
