class BitString:
    def __init__(self, value):
        self._bits = value

    def __add__(self, other):
        if isinstance(other, BitString) and len(self._bits) == len(other._bits):




def ch(x: str, y: str, z: str) -> str:
    length = len(x)
    a = ''
    for i in range(length):
        a += str(int(x[i]) * int(y[i]))
    print(a)


def maj(x, y, z):
    pass


def sigma0(x):
    pass


def sigma1(x):
    pass


if __name__ == '__main__':
    ch('10101', '01110', '')
