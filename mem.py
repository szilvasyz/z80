class genmem():

    def __init__(self, start, size, readonly):
        self.m = {}
        self.ro = False
        for i in range(start, start + size):
            self.m[i] = 0xFF
            self.ro = readonly

    def __setitem__(self, addr, data):
        if not self.ro:
            if addr in self.m.keys():
                self.m[addr] = data
        return

    def __getitem__(self, addr):
        return self.m[addr]

    def keys(self):
        return self.m.keys()

    def load(self, start, data):
        a = start
        for d in data:
            if a in self.m.keys():
                self.m[a] = d
            a = (a + 1) & 0xFFFF

