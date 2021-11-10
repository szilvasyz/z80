class memcon():

    def __init__(self, address):
        self.address = address
        pass

    def __setitem__(self, addr, data):
        if addr == self.address:
            self.writeout(data)
        return

    def __getitem__(self, addr):
        if addr == self.address:
            data = self.readin()
        else:
            data = 0xFF
        return data

    def keys(self):
        return [self.address]

    def writeout(self, data):
        print("{:c}".format(data), end="")

    def readin(self):
        return 0

