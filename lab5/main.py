import json


class BitString:
    def __init__(self, value: str):
        self.bits = value

    def __add__(self, other):
        if isinstance(other, BitString) and len(self.bits) == len(other.bits):
            new_bits = ''

            length = len(self.bits)
            for i in range(length):
                new_bits += str((int(self.bits[i]) + int(other.bits[i])) % 2)

            return BitString(new_bits)

    def __mul__(self, other):
        if isinstance(other, BitString) and len(self.bits) == len(other.bits):
            new_bits = ''

            length = len(self.bits)
            for i in range(length):
                new_bits += str(int(self.bits[i]) * int(other.bits[i]))

            return BitString(new_bits)

    def __floordiv__(self, other):
        if isinstance(other, BitString) and len(self.bits) == len(other.bits):
            return self.bits + other.bits

    def __len__(self):
        return len(self.bits)

    def no(self):
        new_bits = ''

        length = len(self.bits)
        for i in range(length):
            new_bits += str(1 - int(self.bits[i]))

        return BitString(new_bits)

    def csr(self, steps: int):
        new_bits = self.bits[-steps:] + self.bits[:-steps]

        return BitString(new_bits)

    def sr(self, steps: int):
        new_bits = '0' * steps + self.bits[:-steps]

        return BitString(new_bits)

    def split(self, length):
        list_blocks = []

        for i in range(0, len(self.bits), length):
            list_blocks.append(self.bits[i:i + length])

        return list_blocks

    def mod_f_b_in_decimal(self) -> int:
        num = 0
        for i in range(len(self.bits)):
            num += int(self.bits[i]) * 2 ** (len(self.bits) - i - 1)
        return num

    @staticmethod
    def mod_f_d_in_bit(num: int, length):
        if num == 0 and length != 0:
            return '0' * length
        elif num == 0:
            return '0'

        rev_bit_num = []
        while num != 0:
            m = num % 2
            num //= 2
            rev_bit_num.append(str(m))

        zero_list = ['0' for _ in range(length - len(rev_bit_num))]
        rev_bit_num += zero_list

        if length != 0:
            rev_bit_num = rev_bit_num[:length]

        rev_bit_num.reverse()
        bit_num = ''.join(rev_bit_num)
        return BitString(bit_num)


def addition_message(mes: BitString) -> BitString:
    length = len(mes)
    k = (448 - length - 1) % 512

    addition = BitString('1' + '0' * k) // BitString.mod_f_d_in_bit(length, 64)
    new_mes = mes // addition

    return new_mes


def split_message(mes: BitString) -> list[list[BitString]]:
    pass


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
