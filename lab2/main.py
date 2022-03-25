tup_ascii = (' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4',
             '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
             'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^',
             '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
             't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '\x7f')

tup_base64 = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
              'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
              'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+',
              '/')

tup_base32 = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
              'V', 'W', 'X', 'Y', 'Z', '2', '3', '4', '5', '6', '7')


def mod_in_bit(num: int) -> str:
    if num == 0:
        return '0' * 8

    rev_bit_num = []
    while num != 0:
        m = num % 2
        num //= 2
        rev_bit_num.append(str(m))

    zero_list = ['0' for _ in range(8 - len(rev_bit_num))]
    rev_bit_num += zero_list

    rev_bit_num.reverse()
    bit_num = ''.join(rev_bit_num)
    return bit_num


def mod_in_decimal(bit: str) -> int:
    num = 0
    for i in range(len(bit)):
        num += int(bit[i]) * 2 ** (len(bit) - i - 1)
    return num


def cod_base64(message):
    ascii_message = []
    for i in message:
        index = tup_ascii.index(i)
        ascii_message.append(mod_in_bit(32 + index))

    len_ascii_message = len(ascii_message) * 8
    if len_ascii_message % 24 != 0:
        zero_list = ['0' for _ in range(24 - len_ascii_message % 24)]
        ascii_message += zero_list
    else:
        zero_list = []

    ascii_line_message = ''.join(ascii_message)
    bit_base64_message = []
    for i in range(0, len(ascii_line_message), 6):
        bit_base64 = ascii_line_message[i:i+6]
        bit_base64_message.append(bit_base64)

    base64_message = ''
    for i in bit_base64_message:
        base64_message += tup_base64[mod_in_decimal(i)]
    count_equels = len(zero_list) // 8
    base64_message = base64_message[:-count_equels]
    base64_message += count_equels * '='
    return base64_message


def decod_base64(cod_message: str):
    count_equal = cod_message.count('=')
    base64_message = []
    for i in cod_message[:len(cod_message) - count_equal]:
        index = tup_base64.index(i)
        base64_message.append(mod_in_bit(index)[2:])

    ascii_line_message = ''.join(base64_message)
    ascii_line_message = ascii_line_message[:-2 * count_equal]

    bit_ascii_message = []
    for i in range(0, len(ascii_line_message), 8):
        bit_ascii = ascii_line_message[i:i+8]
        bit_ascii_message.append(bit_ascii)

    decod_message = ''
    for i in bit_ascii_message:
        decod_message += tup_ascii[mod_in_decimal(i) - 32]

    return decod_message


def cod_base32(message):
    ascii_message = []
    for i in message:
        index = tup_ascii.index(i)
        ascii_message.append(mod_in_bit(32 + index))

    len_ascii_message = len(ascii_message) * 8
    if len_ascii_message % 40 != 0:
        zero_list = ['0' for _ in range(5 - len_ascii_message % 5)]
        ascii_message += zero_list

    ascii_line_message = ''.join(ascii_message)
    bit_base32_message = []
    for i in range(0, len(ascii_line_message), 5):
        bit_base32 = ascii_line_message[i:i+5]
        bit_base32_message.append(bit_base32)

    base32_message = ''
    for i in bit_base32_message:
        base32_message += tup_base32[mod_in_decimal(i)]

    if len_ascii_message % 5 == 1:
        base32_message += '=' * 4
    elif len_ascii_message % 5 == 2:
        base32_message += '='
    elif len_ascii_message % 5 == 3:
        base32_message += '=' * 6
    elif len_ascii_message % 5 == 4:
        base32_message += '=' * 3

    return base32_message


def decod_base32(cod_message: str):
    count_equal = cod_message.count('=')
    base32_message = []
    for i in cod_message[:len(cod_message) - count_equal]:
        index = tup_base32.index(i)
        base32_message.append(mod_in_bit(index)[3:])

    count_zero = 0
    if count_equal == 1:
        count_zero += 3
    elif count_equal == 3:
        count_zero += 1
    elif count_equal == 4:
        count_zero += 4
    elif count_equal == 6:
        count_zero += 2
    ascii_line_message = ''.join(base32_message)
    ascii_line_message = ascii_line_message[:len(ascii_line_message) - count_zero]

    bit_ascii_message = []
    for i in range(0, len(ascii_line_message), 8):
        bit_ascii = ascii_line_message[i:i + 8]
        bit_ascii_message.append(bit_ascii)

    decod_message = ''
    for i in bit_ascii_message:
        decod_message += tup_ascii[mod_in_decimal(i) - 32]

    return decod_message


def main():
    print('1) Кодирование\n'
          '2) Раскодирование')
    menu = input()

    if menu == '1':
        print('Что будем кодировать?\n'
              '\t1) Сообщение из консоли\n'
              '\t2) Сообщение из файла')
        message_key = input()
        if message_key == '1':
            message = input('Введите соощение: ')
        else:
            path = input('Введите имя файла: ')
            with open(f'{path}.txt', 'r', encoding='utf-8') as file:
                message = file.read()
        print('Выберите метод кодирования\n'
              '\t1) Base64\n'
              '\t2) Base32')
        method_key = input()
        if method_key == '1':
            cod_message = cod_base64(message)
        else:
            cod_message = cod_base32(message)
        name = input('Придумайте имя файла: ')
        with open(f'{name}.txt.cod', 'w', encoding='utf-8') as file:
            file.write(cod_message)
    else:
        path = input('Введите имя файла: ')
        with open(f'{path}.txt.cod', 'r', encoding='utf-8') as file:
            cod_message = file.read()
        print('Выберите метод декодирования\n'
              '\t1) Base64\n'
              '\t2) Base32')
        method_key = input()
        if method_key == '1':
            decod_message = decod_base64(cod_message)
        else:
            decod_message = decod_base32(cod_message)
        name = input('Придумайте имя файла: ')
        with open(f'{name}.txt', 'w', encoding='utf-8') as file:
            file.write(decod_message)


if __name__ == '__main__':
    main()
