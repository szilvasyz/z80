from z80cpu_split import cpu
from mem import genmem
from memcon import memcon

c = cpu()


#
# zexall
#
ram = genmem(0x0000, 0xFFF0, False)
con = memcon(0xFFFF)
c.addmem(ram)
c.addmem(con)

ram.load(0x0000, bytes(open("roms/zexstart.rom", "rb").read()))
ram.load(0x0100, bytes(open("roms/zexall.cim", "rb").read()))

#
# Primo
#
# rom = genmem(0x0000, 0x4000, True)
# ram = genmem(0x4000, 0xA800, False)
# vid = genmem(0xE800, 0x1800, False)
# c.addmem(rom)
# c.addmem(ram)
# c.addmem(vid)
# rom.load(0x0000, bytes(open("roms/PR_A64-1.ROM", "rb").read()))
# rom.load(0x1000, bytes(open("roms/PR_A64-2.ROM", "rb").read()))
# rom.load(0x2000, bytes(open("roms/PR_A64-3.ROM", "rb").read()))
# rom.load(0x3000, bytes(open("roms/PR_A64-4.ROM", "rb").read()))


# ram.load(0x000, [0x31, 0x00, 0x08, 0x21, 0x02, 0x00, 0x06, 0x03, 0xCD, 0x00, 0x01, 0x10, 0xFB, 0x76])
# ram.load(0x100, [0x4F, 0xAE, 0x23, 0xC9])
#
# ram.load(0x000, [0x06, 0xAA, 0xCB, 0x00, 0x31, 0x00, 0x08, 0xC3, 0x00, 0x01])
# ram.load(0x100, [0x21, 0x00, 0x02, 0x4E, 0x23, 0x46, 0x23, 0xC5, 0xF1, 0x7E, 0x98, 0xF5, 0xD1, 0x76])
# ram.load(0x200, [0x01, 0x7F, 0x80])

# for i in range(256):
#     c.wrmem(0, 0xed)
#     c.wrmem(1, i)
#     c.wrmem(2, 0)
#     c.wrmem(3, i)
#     c.r["PC"] = 0
#     c.step()


brkpts = []

while not c.halted:
    if c.r["PC"] in brkpts:
        print("BRK at {:04X}".format(c.r["PC"]))
        print(c.r)
        print(" --- ")

    s = c.step()
#    print(c.r)

print(c.r)
