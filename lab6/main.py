from stribog import stribog, x
from sha import sha256, sha512

from BitString import BitString
from random import randint
from pmf import pmf

size_block_for_h = {
    stribog: 512,
    sha256: 512,
    sha512: 1024
}


def hcam_sha(key: BitString, message: BitString, func) -> BitString:

    ipad = BitString('00110110' * (size_block_for_h[func] // 8))
    opad = BitString('01011100' * (size_block_for_h[func] // 8))

    return func((key + opad) // func((key + ipad) // message))


def hcam_stribog(key, message, func, func_key):

    ipad = '00110110' * (size_block_for_h[func] // 8)
    opad = '01011100' * (size_block_for_h[func] // 8)

    return func(x(key, opad) + func(x(key, ipad) + message, func_key), func_key)


def gen_key() -> BitString:
    key = BitString.mod_f_d_in_bit(pmf(randint(100, 300), 100), 0)

    return key


def format_key(key, func):
    zero_bit = BitString('0' * (size_block_for_h[func] - len(key)))
    key //= zero_bit

    return key


def get_key():
    name = input('\nВведите имя файла: ')
    with open(f'{name}.key', 'r') as file:
        key = file.read()

    return BitString(key)


def save_key(key):
    name = input('\nВведите имя файла: ')
    with open(f'{name}.key', 'w') as file:
        file.write(key)


def menu():
    print('Откуда будем кодировать?\n'
          '\t1) Сообщение из консоли\n'
          '\t2) Сообщение из файла')
    message_key = input()

    if message_key == '1':
        message = input('Введите соощение: ')
    else:
        path = input('Введите имя файла: ')
        with open(f'{path}.txt', 'r', encoding='utf-8') as file:
            message = file.read()

    key_menu = input('\nВыберите метод хеширования:\n'
                     '\t1) SHA-512;\n'
                     '\t2) SHA-256;\n'
                     '\t3) Stribog-512;\n'
                     '\t4) Stribog-256\n')

    menu_for_key = input('\nВыберите ключ:\n'
                         '\t1) Создать ключ;\n'
                         '\t2) Воспользоваться имеющимся\n')

    key = ''
    if menu_for_key == '1':
        key = gen_key()
        save_key(key.bits)
    elif menu_for_key == '2':
        key = get_key()

    message = BitString.mod_text_in_bit(message)

    if key_menu == '1':
        key = format_key(key, sha512)
        print(hcam_sha(key, message, sha512).mod_f_b_in_16())
    elif key_menu == '2':
        key = format_key(key, sha256)
        print(hcam_sha(key, message, sha256).mod_f_b_in_16())
    elif key_menu == '3':
        key = format_key(key, stribog)
        message = message.bits
        print(BitString(hcam_stribog(key.bits, message, stribog, '1')).mod_f_b_in_16())
    elif key_menu == '4':
        key = format_key(key, stribog)
        message = message.bits
        print(BitString(hcam_stribog(key.bits, message, stribog, '2')).mod_f_b_in_16())


if __name__ == '__main__':
    menu()
