TUP_16 = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')


PI = (252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77, 233, 119, 240, 219, 147, 46, 153, 186,
      23, 54, 241, 187, 20, 205, 95, 193, 249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79, 5, 132,
      2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31, 235, 52, 44, 81, 234, 200, 72, 171, 242, 42, 104,
      162, 253, 58, 206, 204, 181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156, 183, 93, 135, 21, 161, 150, 41,
      16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178, 177, 50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128,
      195, 189, 13, 87, 223, 245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3, 224, 15, 236, 222,
      122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74, 167, 151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100,
      159, 38, 65, 173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213, 149, 59, 7, 88, 179, 64, 134, 172,
      29, 247, 48, 55, 107, 228, 136, 217, 231, 137, 225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216,
      133, 97, 32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82, 89, 166, 116, 210, 230, 244, 180,
      192, 209, 102, 175, 194, 57, 75, 99, 182)


R = (0, 8, 16, 24, 32, 40, 48, 56, 1,9, 17, 25, 33, 41, 49, 57, 2, 10, 18, 26, 34, 42, 50, 58, 3, 11, 19, 27, 35, 43,
     51, 59, 4, 12, 20, 28, 36, 44, 52, 60, 5, 13, 21, 29, 37, 45, 53, 61, 6, 14, 22, 30, 38, 46, 54, 62, 7, 15, 23, 31,
     39, 47, 55, 63)


A = ('8e20faa72ba0b470', '47107ddd9b505a38', 'ad08b0e0c3282d1c', 'd8045870ef14980e', '6c022c38f90a4c07',
     '3601161cf205268d', '1b8e0b0e798c13c8', '83478b07b2468764', 'a0116380818e8f40', '5086e740ce47c920',
     '2843fd2067adea10', '14aff010bdd87508', '0ad97808d06cb404', '05e23c0468365a02', '8c711e02341b2d01',
     '46b60f011a83988e', '90dab52a387ae76f', '486dd4151c3dfdb9', '24b86a840e90f0d2', '125c354207487869',
     '092e94218d243cba', '8a174a9ec8121e5d', '4585254f64090fa0', 'accc9ca9328a8950', '9d4df05d5f661451',
     'c0a878a0a1330aa6', '60543c50de970553', '302a1e286fc58ca7', '18150f14b9ec46dd', '0c84890ad27623e0',
     '0642ca05693b9f70', '0321658cba93c138', '86275df09ce8aaa8', '439da0784e745554', 'afc0503c273aa42a',
     'd960281e9d1d5215', 'e230140fc0802984', '71180a8960409a42', 'b60c05ca30204d21', '5b068c651810a89e',
     '456c34887a3805b9', 'ac361a443d1c8cd2', '561b0d22900e4669', '2b838811480723ba', '9bcf4486248d9f5d',
     'c3e9224312c8c1a0', 'effa11af0964ee50', 'f97d86d98a327728', 'e4fa2054a80b329c', '727d102a548b194e',
     '39b008152acb8227', '9258048415eb419d', '492c024284fbaec0', 'aa16012142f35760', '550b8e9e21f7a530',
     'a48b474f9ef5dc18', '70a6a56e2440598e', '3853dc371220a247', '1ca76e95091051ad', '0edd37c48a08a6d8',
     '07e095624504536c', '8d70c431ac02a736', 'c83862965601dd1b', '641c314b2b8ee083')


def mod_f_d_in_bit(num: int) -> str:
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


def mod_f_b_in_16(bit: str) -> str:
    str16 = ''
    for i in range(0, len(bit), 4):
        num = mod_f_b_in_decimal(bit[i:i + 4])
        str16 += TUP_16[num]
    return str16


def mod_f_16_in_b(str16: str) -> str:
    str_bit = ''
    for i in str16:
        str_bit += mod_f_d_in_bit(TUP_16.index(i))[4:]
    return str_bit


def mod_f_b_in_decimal(bit: str) -> int:
    num = 0
    for i in range(len(bit)):
        num += int(bit[i]) * 2 ** (len(bit) - i - 1)
    return num


def s(bits: str) -> str:
    s_string = ''
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        num = mod_f_b_in_decimal(byte)
        pi_num = PI[num]
        s_string += mod_f_d_in_bit(pi_num)

    return s_string


def p(bits: str) -> str:
    p_list_string = ['' for _ in range(64)]
    index = 0
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        p_index = R[index]
        p_list_string[p_index] = byte
        index += 1

    p_string = ''.join(p_list_string)
    return p_string


def l(bits: str) -> str:
    bit_a = [mod_f_16_in_b(i) for i in A]
    vec_matrix = []
    for i in range(0, len(bits), 64):
        vec_matrix.append(bits[i:i+64])

    length = 64
    new_vec_matrix = [[0 for i in range(length)] for i in range(len(vec_matrix))]
    for i in range(len(vec_matrix)):
        for j in range(length):
            for k in range(length):

                mul = int(vec_matrix[i][k]) * int(bit_a[k][j])
                if new_vec_matrix[i][j] == 1 and mul == 1:
                    new_vec_matrix[i][j] = 0
                else:
                    new_vec_matrix[i][j] += mul

                if k == length - 1:
                    new_vec_matrix[i][j] = str(new_vec_matrix[i][j])

    for i in range(len(new_vec_matrix)):
        new_vec_matrix[i] = ''.join(new_vec_matrix[i])

    return ''.join(new_vec_matrix)


if __name__ == '__main__':
    S = s('0' * 512)
    P = p(S)
    l(P)
