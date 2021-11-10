class flags:

    def __init__(self, reg):
        self.reg = reg
        self.flagbit = {"S": 0b10000000, "Z": 0b01000000, "5": 0b00100000, "H": 0b00010000,
                        "3": 0b00001000, "P": 0b00000100, "N": 0b00000010, "C": 0b00000001}

    def __setitem__(self, flag, bit):
        if bit:
            self.reg["F"] |= self.flagbit[flag]
        else:
            self.reg["F"] &= ~self.flagbit[flag]

    def __getitem__(self, flag):
        return 1 if self.reg["F"] & self.flagbit[flag] else 0

    def __str__(self):
        return "SZ5H3PNC\n" + ("0000000" + bin(self.reg["F"])[2:])[-8:]

