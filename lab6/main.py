from stribog import stribog, x
from sha import sha256, sha512

from BitString import BitString
from pmf import pmf


size_block_for_h = {
    stribog: 512,
    sha256: 256,
    sha512: 512
}


def hcam_sha(key: BitString, message: BitString, func) -> BitString:

    ipad = BitString('00110110' * (size_block_for_h[func] // 8))
    opad = BitString('01011100' * (size_block_for_h[func] // 8))

    return func((key + opad) // func((key + ipad) // message))


def hcam_stribog(key, message, func, func_key):

    ipad = '00110110' * (size_block_for_h[func] // 8)
    opad = '01011100' * (size_block_for_h[func] // 8)

    return func(x(key, opad) + func(x(key, ipad) + message, func_key), func_key)


def gen_key(func) -> BitString:
    key = BitString.mod_f_d_in_bit(pmf(100, 100), 0)
    zero_bit = BitString('0' * (size_block_for_h[func] - len(key)))
    key //= zero_bit

    return key


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

    message = BitString.mod_text_in_bit(message).bits

    if key_menu == '1':
        key = gen_key(sha512)
        print(hcam_sha(key, message, sha512).mod_f_b_in_16())
    elif key_menu == '2':
        key = gen_key(sha256)
        print(hcam_sha(key, message, sha256).mod_f_b_in_16())
    elif key_menu == '3':
        key = gen_key(stribog)
        print(BitString(hcam_stribog(key.bits, message, stribog, 1)).mod_f_b_in_16())
    elif key_menu == '4':
        key = gen_key(stribog)
        print(BitString(hcam_stribog(key.bits, message, stribog, 2)).mod_f_b_in_16())


if __name__ == '__main__':
    menu()
