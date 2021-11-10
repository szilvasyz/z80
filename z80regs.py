from utils import *
from z80flags import flags


class registers():

    def __init__(self, cpu):
        self.cpu = cpu
        self.flag = flags(self)
        self.regs = {'B': 0, 'C': 0,
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
            self.regs[reg] = word(value)
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
            return mkword(self.regs[reg[0]], self.regs[reg[1]])

        if reg in ["IX", "IY"]:
            return mkword(self.regs[reg[1] + "H"], self.regs[reg[1] + "L"])

        return self.regs[reg]

    def __str__(self):
        s = "_BC_ _DE_ _HL_ _AF_ _IX_ _IY_ _PC_ _SP_ _I _R\n" \
            "{:04X} {:04X} {:04X} {:04X} {:04X} {:04X} {:04X} {:04X} {:02X} {:02X} "
        return (s.format(
            self["BC"], self["DE"], self["HL"],
            self["AF"], self["IX"], self["IY"],
            self["PC"], self["SP"], self["I"], self["R"])
        )

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
