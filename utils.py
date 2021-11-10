rname = ["B", "C", "D", "E", "H", "L", "M", "A"]
rxname = ["B", "C", "D", "E", "XH", "XL", "M", "A"]
ryname = ["B", "C", "D", "E", "YH", "YL", "M", "A"]
rpname = ["BC", "DE", "HL", "SP"]
rpxname = ["BC", "DE", "IX", "SP"]
rpyname = ["BC", "DE", "IY", "SP"]
rp2name = ["BC", "DE", "HL", "AF"]
rp2xname = ["BC", "DE", "IX", "AF"]
rp2yname = ["BC", "DE", "IY", "AF"]


def add8(op1, op2, cy):
    res = lobyte(op1 + op2 + cy)
    f = 0
    f |= ((op1 & 0xF) + (op2 & 0xF) + cy) & 0x10  # h
    f |= (op1 + op2 + cy) >> 8  # c
    f |= res & 0x80  # s
    f |= 0 if (op1 ^ op2) & 0x80 else ((op1 ^ res) >> 5) & 0x4  # v
    f |= 0 if res else 0x40  # z
    f |= res & 0x28  # f3, f5
    return [res, f]


def sub8(op1, op2, cy):
    res = lobyte(op1 - op2 - cy)
    f = 2  # n
    f |= ((op1 & 0xF) - (op2 & 0xF) - cy) & 0x10  # h
    f |= ((op1 - op2 - cy) >> 8) & 1  # c
    f |= res & 0x80  # s
    f |= ((op1 ^ res) >> 5) & 0x4 if (op1 ^ op2) & 0x80 else 0  # v
    f |= 0 if res else 0x40  # z
    f |= res & 0x28  # f3, f5
    return [res, f]


def add16(op1, op2, cy):
    rl = lobyte(op1) + lobyte(op2) + cy
    c = rl >> 8
    rl = lobyte(rl)
    oh1 = hibyte(op1)
    oh2 = hibyte(op2)
    rh = lobyte(oh1 + oh2 + c)
    f = 0
    f |= ((oh1 & 0xF) + (oh2 & 0xF) + c) & 0x10  # h
    f |= (oh1 + oh2 + c) >> 8  # c
    f |= rh & 0x80  # s
    f |= 0 if (oh1 ^ oh2) & 0x80 else ((oh1 ^ rh) >> 5) & 0x4  # v
    f |= 0 if rh or rl else 0x40  # z
    f |= rh & 0x28  # f3, f5
    return [(rh << 8) | rl, f]


def sub16(op1, op2, cy):
    rl = lobyte(op1) - lobyte(op2) - cy
    c = rl >> 8
    rl = lobyte(rl)
    oh1 = hibyte(op1)
    oh2 = hibyte(op2)
    rh = lobyte(oh1 - oh2 - c)
    f = 2  # n
    f |= ((oh1 & 0xF) - (oh2 & 0xF) - c) & 0x10  # h
    f |= (oh1 - oh2 - c) >> 8  # c
    f |= rh & 0x80  # s
    f |= ((oh1 ^ rh) >> 5) & 0x4 if (oh1 ^ oh2) & 0x80 else 0  # v
    f |= 0 if rh or rl else 0x40  # z
    f |= rh & 0x28  # f3, f5
    return [(rh << 8) | rl, f]


def rotfun(d, c, fun):
    rv = fun(d, c)
    rv[0] &= 0xFF
    rv[1] = (rv[1] & 0x01) | logf(rv[0])
    return rv


def logf(op):
    p = op ^ (op >> 4)
    p = p ^ (p >> 2)
    p = p ^ (p >> 1)
    f = 0 if p & 1 else 4
    f |= op & 0x80  # s
    f |= 0 if op else 0x40  # z
    f |= op & 0x08  # f3
    f |= op & 0x20  # f5
    return f


def lobyte(i):
    return i & 0xFF


def hibyte(i):
    return (i >> 8) & 0xff


def word(i):
    return i & 0xFFFF


def mkword(h, l):
    return (lobyte(h) << 8) | lobyte(l)


def signdsp(d):
    if d & 0x80:
        d = d - 0x100
    return d


def adddsp(a, d):
    return word(a + signdsp(d))


def inc8(i):
    return lobyte(i + 1)


def dec8(i):
    return lobyte(i - 1)


def inc16(i):
    return word(i + 1)


def dec16(i):
    return word(i - 1)


