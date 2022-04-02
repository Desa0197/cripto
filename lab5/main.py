import json


class BitString:
    def __init__(self, value: str):
        self._bits = value

    def __add__(self, other):
        if isinstance(other, BitString) and len(self._bits) == len(other._bits):
            new_bits = ''

            length = len(self._bits)
            for i in range(length):
                new_bits += str((int(self._bits[i]) + int(other._bits[i])) % 2)

            return BitString(new_bits)

    def __mul__(self, other):
        if isinstance(other, BitString) and len(self._bits) == len(other._bits):
            new_bits = ''

            length = len(self._bits)
            for i in range(length):
                new_bits += str(int(self._bits[i]) * int(other._bits[i]))

            return BitString(new_bits)

    def no(self):
        new_bits = ''

        length = len(self._bits)
        for i in range(length):
            new_bits += str(1 - int(self._bits[i]))

        return BitString(new_bits)

    def csr(self, steps: int):
        new_bits = self._bits[-steps:] + self._bits[:-steps]

        return BitString(new_bits)

    def sr(self, steps: int):
        new_bits = '0' * steps + self._bits[:-steps]

        return BitString(new_bits)


def ch(x: BitString, y: BitString, z: BitString) -> BitString:
    return x * y + x.no() * z


def maj(x: BitString, y: BitString, z: BitString) -> BitString:
    return x * y + x * z + y * z


def s0(x: BitString) -> BitString:
    return x.csr(2) + x.csr(13) + x.csr(22)


def s1(x: BitString) -> BitString:
    return x.csr(6) + x.csr(11) + x.csr(25)


def sigma0(x: BitString) -> BitString:
    return x.csr(7) + x.csr(18) + x.sr(3)


def sigma1(x: BitString) -> BitString:
    return x.csr(17) + x.csr(19) + x.sr(10)


if __name__ == '__main__':
    # ch('10101', '01110', '')
    pass


