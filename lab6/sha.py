from BitString import BitString
import json


def read_file(method):
    with open(f'const{method}.json', 'r') as file:
        dict_consts = json.load(file)

    list_k = []
    list_h = []
    for i in dict_consts['k']:
        list_k.append(BitString.mod_f_16_in_b(i))
    for i in dict_consts['h']:
        list_h.append(BitString.mod_f_16_in_b(i))

    return [list_k, list_h]


def addition_message_256(mes: BitString) -> BitString:
    length = len(mes)
    k = (448 - length - 1) % 512

    addition = BitString('1' + '0' * k) // BitString.mod_f_d_in_bit(length, 64)
    new_mes = mes // addition

    return new_mes


def split_message_256(mes: BitString) -> list[list[BitString]]:
    blocks512 = mes.split(512)
    blocks512_32 = []
    for i in blocks512:
        blocks512_32.append(i.split(32))

    return blocks512_32


def create_w64(block512_32: list[BitString]) -> list[BitString]:
    list_w64 = block512_32

    for i in range(16, 64):
        w = (list_w64[i - 16].mod_f_b_in_decimal() + sigma0(list_w64[i - 15]).mod_f_b_in_decimal() +
             list_w64[i - 7].mod_f_b_in_decimal() + sigma1(list_w64[i - 2]).mod_f_b_in_decimal()) % 2 ** 32
        list_w64.append(BitString.mod_f_d_in_bit(w, 32))

    return list_w64


def compression(list_w64, list_h: list[BitString], list_k):
    tc = list_h[:]

    for i in range(len(list_w64)):
        temp1 = BitString.mod_f_d_in_bit((tc[7].mod_f_b_in_decimal() + s1(tc[4]).mod_f_b_in_decimal() + ch(tc[4], tc[5], tc[6]).mod_f_b_in_decimal() + list_w64[i].mod_f_b_in_decimal() + list_k[i].mod_f_b_in_decimal()) % 2 ** 32, 32)
        temp2 = BitString.mod_f_d_in_bit((s0(tc[0]).mod_f_b_in_decimal() + maj(tc[0], tc[1], tc[2]).mod_f_b_in_decimal()) % 2 ** 32, 32)
        tc[7] = tc[6]
        tc[6] = tc[5]
        tc[5] = tc[4]
        tc[4] = BitString.mod_f_d_in_bit((tc[3].mod_f_b_in_decimal() + temp1.mod_f_b_in_decimal()) % 2 ** 32, 32)
        tc[3] = tc[2]
        tc[2] = tc[1]
        tc[1] = tc[0]
        tc[0] = BitString.mod_f_d_in_bit((temp1.mod_f_b_in_decimal() + temp2.mod_f_b_in_decimal()) % 2 ** 32, 32)

    for i in range(len(list_h)):
        list_h[i] = BitString.mod_f_d_in_bit((list_h[i].mod_f_b_in_decimal() + tc[i].mod_f_b_in_decimal()) % 2 ** 32, 32)
    return list_h


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


def sha256(mes: BitString):
    add_mes = addition_message_256(mes) # дополняем сообщение
    blocks512_32 = split_message_256(add_mes) # делим на блоки по 512 / 32

    list_k, list_h = read_file(256)

    for i in blocks512_32:
        list_w64 = create_w64(i)
        list_h = compression(list_w64, list_h, list_k)

    return BitString.join(list_h)


def addition_message_512(mes: BitString) -> BitString:
    length = len(mes)
    k = (896 - length - 1) % 1024

    addition = BitString('1' + '0' * k) // BitString.mod_f_d_in_bit(length, 128)
    new_mes = mes // addition

    return new_mes


def split_message_512(mes: BitString) -> list[list[BitString]]:
    blocks1024 = mes.split(1024)
    blocks1024_64 = []
    for i in blocks1024:
        blocks1024_64.append(i.split(64))

    return blocks1024_64


def create_w80(block1024_64: list[BitString]) -> list[BitString]:
    list_w80 = block1024_64

    for i in range(16, 80):
        w = (list_w80[i - 16].mod_f_b_in_decimal() + sigma0_512(list_w80[i - 15]).mod_f_b_in_decimal() +
             list_w80[i - 7].mod_f_b_in_decimal() + sigma1_512(list_w80[i - 2]).mod_f_b_in_decimal()) % 2 ** 64
        list_w80.append(BitString.mod_f_d_in_bit(w, 64))

    return list_w80


def compression_512(list_w80, list_h: list[BitString], list_k):
    tc = list_h[:]

    for i in range(len(list_w80)):
        temp1 = BitString.mod_f_d_in_bit((tc[7].mod_f_b_in_decimal() + s1_512(tc[4]).mod_f_b_in_decimal() + ch(tc[4], tc[5], tc[6]).mod_f_b_in_decimal() + list_w80[i].mod_f_b_in_decimal() + list_k[i].mod_f_b_in_decimal()) % 2 ** 64, 64)
        temp2 = BitString.mod_f_d_in_bit((s0_512(tc[0]).mod_f_b_in_decimal() + maj(tc[0], tc[1], tc[2]).mod_f_b_in_decimal()) % 2 ** 64, 64)
        tc[7] = tc[6]
        tc[6] = tc[5]
        tc[5] = tc[4]
        tc[4] = BitString.mod_f_d_in_bit((tc[3].mod_f_b_in_decimal() + temp1.mod_f_b_in_decimal()) % 2 ** 64, 64)
        tc[3] = tc[2]
        tc[2] = tc[1]
        tc[1] = tc[0]
        tc[0] = BitString.mod_f_d_in_bit((temp1.mod_f_b_in_decimal() + temp2.mod_f_b_in_decimal()) % 2 ** 64, 64)

    for i in range(len(list_h)):
        list_h[i] = BitString.mod_f_d_in_bit((list_h[i].mod_f_b_in_decimal() + tc[i].mod_f_b_in_decimal()) % 2 ** 64, 64)

    return list_h


def s0_512(x: BitString) -> BitString:
    return x.csr(28) + x.csr(34) + x.csr(39)


def s1_512(x: BitString) -> BitString:
    return x.csr(14) + x.csr(18) + x.csr(41)


def sigma0_512(x: BitString) -> BitString:
    return x.csr(1) + x.csr(8) + x.sr(7)


def sigma1_512(x: BitString) -> BitString:
    return x.csr(19) + x.csr(61) + x.sr(6)


def sha512(mes: BitString):
    add_mes = addition_message_512(mes) # дополняем сообщение
    blocks1024_64 = split_message_512(add_mes) # делим на блоки по 512 / 32

    list_k, list_h = read_file(512)

    for i in blocks1024_64:
        list_w80 = create_w80(i)

        list_h = compression_512(list_w80, list_h, list_k)
    return BitString.join(list_h)
