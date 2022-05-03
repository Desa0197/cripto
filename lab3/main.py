from random import randint
import json
from BitString import BitString as bs


def pmf(k, t):
    while True:
        p = ""
        for i in range(k - 2):
            p = str(randint(0, 1)) + p
        p = "1" + p + '1'
        p = int(p, 2)
        flag = 1
        if p == 2:
            return True
        if not p & 1:
            return False

        def check(a, s, d, p):
            x = pow(a, d, p)
            if x == 1:
                return True
            for i in range(s - 1):
                if x == p - 1:
                    return True
                x = pow(x, 2, p)
            return x == p - 1

        s = 0
        d = p - 1
        while d % 2 == 0:
            d >>= 1
            s += 1
        for i in range(t):
            a = randint(2, p - 2)
            if not check(a, s, d, p):
                flag = 0
        if flag == 1:
            return p


def Evklide(x, y):
    a2 = 1
    a1 = 0
    b2 = 0
    b1 = 1
    while y != 0:
        q = x // y
        r = x - q * y
        a = a2 - q * a1
        b = b2 - q * b1
        x = y
        y = r
        a2 = a1
        a1 = a
        b2 = b1
        b1 = b
    m = x
    a = a2
    b = b2

    if m == 1:
        return b
    else:
        return 0
    # print(f"НОД(x,y)={m} \n Его линейное представление выглядит {a}*{x}+{b}*{y}={m} ")


def addition_message(message, len_block):
    remains = (len_block - len(message) % len_block)
    new_mes = []

    for i in range(0, len(message), len_block):
        block = message[i:i + len_block]
        if len(block) == len_block:
            new_mes += block + [0]
        else:
            new_mes += block + [remains] * (remains + 1)

    return new_mes


def save_key(n, e, p, q, d):
    open_key = {
        "SubjectPublicKeyInfo":
            {
                "publicExponent": e,
                "N": n
            }
    }

    q1 = Evklide(p, q)

    close_key = {
        "privateExponent": d,
        "prime1": p,
        "prime2": q,
        "exponent1": d % (p - 1),
        "exponent2": d % (q - 1),
        "coefficient": q1 % p
    }

    name_file = input('Введите имя файла ключа: ')
    with open(f'{name_file}.open_key.json', 'w') as file:
        json.dump(open_key, file, indent=4)

    with open(f'{name_file}.close_key.json', 'w') as file:
        json.dump(close_key, file, indent=4)


def encrypt(message, e, n, size_block):
    block_bit = bs()
    for i in message:
        block_bit //= bs.mod_f_d_in_bit(i, 8)

    en_mes_int = pow(int(str(block_bit), 2), e, n)
    bit_en_mes = bs.mod_f_d_in_bit(en_mes_int, size_block * 8)

    return bit_en_mes


def decrypt(message, d, n, size_block):
    block_bit = bs()
    for i in message:
        block_bit //= bs.mod_f_d_in_bit(i, 8)

    en_mes_int = pow(int(str(block_bit), 2), d, n)
    bit_en_mes = bs.mod_f_d_in_bit(en_mes_int, (size_block - 1) * 8)

    block_byte = bit_en_mes.mod_f_b_in_byte()
    origin_block = block_byte[:-(block_byte[-1]) - 1]

    origin_block_bit = bs()
    for i in origin_block:
        origin_block_bit //= bs.mod_f_d_in_bit(i, 8)

    return origin_block_bit


def rsa():
    d = 0
    e = 0

    key_menu = input('1) Создать ключ;\n'
                     '2) Воспользоваться существующим\n')

    if key_menu == '1':
        p = pmf(100, 100)
        q = pmf(100, 100)
        n = p * q
        x = (p - 1) * (q - 1)

        while d == 0:
            e = int(input(f'Введите число меньше {x}: '))
            d = Evklide(x, e)

        save_key(n, e, p, q, d)

    else:
        file_name = input('Введите имя файла открытого ключа: ')
        with open(f'{file_name}.open_key.json', 'w') as file:
            open_key = json.load(file)
            e = open_key['SubjectPublicKeyInfo']['publicExponent']
            n = open_key['SubjectPublicKeyInfo']['N']

    bit_n = bs.mod_f_d_in_bit(n, len(bs.mod_f_d_in_bit(n, 0)) + 8 - len(bs.mod_f_d_in_bit(n, 0)) % 8)
    byte_n = bit_n.mod_f_b_in_byte()

    size_block = len(byte_n) - 2

    message = input('Ввеведите текст: ')
    m = bs.mod_text_in_bit(message).mod_f_b_in_byte()
    mes = addition_message(m, size_block)

    en_mes = bs()
    for i in range(0, len(mes), size_block + 1):
        block = mes[i:i + size_block + 1]
        en_block = encrypt(block, e, n, size_block + 2)
        en_mes //= en_block

    en_mes16 = en_mes.mod_f_b_in_16()

    data_encrypt = {
        "Version": 0,
        "EncryptedContentInfo": {
            "ContentType": "text",
            "ContentEncryptionAlgorithmIdentifier": "rsaEncryption",
            "encryptedContent": en_mes16,
            "OPTIONAL": ""
        }
    }

    name_file = input('Введите имя файла, в который сохраним шифр-текст: ')
    with open(f'{name_file}.encrypt.json', 'w', encoding='utf-8') as file:
        json.dump(data_encrypt, file, indent=4)


def decrypt_rsa():
    name_file = input('Введите имя файла шифр-текста: ')
    with open(f'{name_file}.encrypt.json', 'r') as file:
        data_en = json.load(file)
        en_mes = data_en['EncryptedContentInfo']['encryptedContent']

    name_file = input('Введите имя файла закрытого ключа: ')
    with open(f'{name_file}.close_key.json', 'r') as file:
        data_en = json.load(file)
        d = data_en['privateExponent']
        p = data_en['prime1']
        q = data_en['prime2']
    n = p * q

    bit_n = bs.mod_f_d_in_bit(n, len(bs.mod_f_d_in_bit(n, 0)) + 8 - len(bs.mod_f_d_in_bit(n, 0)) % 8)
    size_block = len(bit_n.mod_f_b_in_byte())

    en_mes_byte = bs.mod_f_16_in_b(en_mes).mod_f_b_in_byte()

    de_mes = bs()
    for i in range(0, len(en_mes_byte), size_block):
        en_block_byte = en_mes_byte[i:i + size_block]
        de_block = decrypt(en_block_byte, d, n, size_block)
        de_mes //= de_block

    mes = int(str(de_mes), 2).to_bytes(len(de_mes) // 8, byteorder='big').decode('utf-8')
    print(mes)


if __name__ == '__main__':
    decrypt_rsa()
