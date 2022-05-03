TUP_16 = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')


class BitString:
    def __init__(self, value=''):
        self.bits = value

    def __str__(self):
        return self.bits

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
        if isinstance(other, BitString):
            return BitString(self.bits + other.bits)

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
            list_blocks.append(BitString(self.bits[i:i + length]))

        return list_blocks

    def mod_f_b_in_decimal(self) -> int:
        num = 0
        for i in range(len(self.bits)):
            num += int(self.bits[i]) * 2 ** (len(self.bits) - i - 1)
        return num

    def mod_f_b_in_16(self):
        str16 = ''
        for i in range(0, len(self.bits), 4):
            num = BitString.mod_f_b_in_decimal(BitString(self.bits[i:i + 4]))
            str16 += TUP_16[num]
        return str16

    def mod_f_b_in_byte(self):
        byte = []
        for i in range(0, len(self.bits), 8):
            num = BitString.mod_f_b_in_decimal(BitString(self.bits[i:i + 8]))
            byte.append(num)
        return byte

    @staticmethod
    def join(list_bits):
        new_str_bits = ''
        for i in list_bits:
            new_str_bits += i.bits

        return BitString(new_str_bits)

    @staticmethod
    def mod_f_d_in_bit(num: int, length):
        if num == 0 and length != 0:
            return BitString('0' * length)
        elif num == 0:
            return BitString('0')

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

    @staticmethod
    def mod_f_16_in_b(str16: str):
        str_bit = BitString.mod_f_d_in_bit(TUP_16.index(str16[0]), 4)
        for i in range(1, len(str16)):
            str_bit = str_bit // BitString.mod_f_d_in_bit(TUP_16.index(str16[i]), 4)
        return str_bit

    @staticmethod
    def mod_text_in_bit(text):
        bit_text = ''
        encode_text = text.encode('utf-8')

        for i in range(len(encode_text)):
            bit_text = bit_text + '0' * (8 - len(format(encode_text[i], 'b'))) + format(encode_text[i], 'b')

        return BitString(bit_text)