import random

def simbol_iakobi(rund_int, mb_simple, g=1):
    a, n, g, s = rund_int, mb_simple, g, 0
    if a == 0:
        return 0
    elif a == 1:
        return g
    find_pow_a = a
    pow = 0
    while True:
        if find_pow_a % 2 == 0:
            pow += 1
        else:
            break
        find_pow_a = int(find_pow_a / 2)
    a1 = find_pow_a
    if pow % 2 == 0:
        s += 1
    else:
        if n % 8 == 1 or n % 8 == 7:
            s += 1
        elif n % 8 == 3 or n % 8 == 5:
            s -= 1
    if a1 == 1:
        return g * s

    if n % 4 == 3 and a1 % 4 == 3:
        s = -s

    a, n, g = n % a1, a1, g * s
    return simbol_iakobi(a, n, g)


def test_ferma(mb_simple_num):
    count = 0
    n = mb_simple_num
    for i in range(1000):
        a = random.randint(2, n-2)
        pow_a = a ** (n-1)
        r = pow_a % n
        if r == 1:
            count += 1
    if count == 1000:
        print("Число вероятно простое")
    else:
        ver = count / 10
        print(f"Число составное.\n Вероятность ошибки {ver}%")

def test_soloveia(mb_simple_num):
    count = 0
    n = mb_simple_num
    for i in range(1000):
        a = random.randint(2, n-2)
        r = pow(a, (n - 1) // 2, n)
        if r == 1 or r == n-1:
            iakobi = simbol_iakobi(a, n)
            if iakobi < 0:
                iakobi = n-1
            if r == iakobi:
                count += 1
    if count == 1000:
        print("Число вероятно простое")
    else:
        ver = count / 10
        print(f"Число составное.\n Вероятность ошибки {ver}%")


def test_rabina(mb_simple_num):
    count = 0
    n = mb_simple_num
    for i in range(1000):
        a = random.randint(2, n-2)
        find_pow_n = n - 1
        s = 0
        while True:
            if find_pow_n % 2 == 0:
                s += 1
            else:
                break
            find_pow_n = int(find_pow_n / 2)
        r = find_pow_n
        y = []
        y.append(a ** r % n)
        j=0
        if y[0] != 1 and y[0] != n-1:
            j += 1
            while j <= s-1 and y[0] != n-1:
                y[0] = y[0] ** 2 % n
                if y[0] == 1:
                    break
                else:
                    j += 1
            if y[0] != n - 1:
                continue
            else:
                count += 1
        else:
            count += 1
    if count == 1000:
        print("Число вероятно простое")
    else:
        ver = count / 10
        print(f"Число составное.\n Вероятность ошибки {ver}%")


def test_rabina_for_find_simple_namber(mb_simple_number, a):
    find_pow_mb_simple_number = mb_simple_number - 1
    s = 0
    while True:
        if find_pow_mb_simple_number % 2 == 0:
            s += 1
        else:
            break
        find_pow_mb_simple_number = int(find_pow_mb_simple_number / 2)
    r = find_pow_mb_simple_number
    y = []
    y.append(a ** r % mb_simple_number)
    j = 0
    if y[0] != 1 and y[0] != mb_simple_number - 1:
        j += 1
        while j <= s - 1 and y[0] != mb_simple_number - 1:
            y[0] = y[0] ** 2 % mb_simple_number
            if y[0] == 1:
                break
            else:
                j += 1
        if y[0] != mb_simple_number - 1:
            return False
        else:
            return True
    else:
        return True


def generation_simple_number():
    k = int(input("Введите разрядность: "))
    t = int(input("Введите параметр t больше нуля: "))

    list_mb_simple_number = []
    for i in range(k):
        if i == 0 or i == k - 1:
            list_mb_simple_number.append(1)
        else:
            list_mb_simple_number.append(random.randint(0, 1))
    mb_simple_number = 0
    for i in range(1, k + 1):
        mb_simple_number += list_mb_simple_number[-i] * pow(2, i - 1)

    for i in range(t):
        a = random.randint(2, mb_simple_number - 2)
        if test_rabina_for_find_simple_namber(mb_simple_number, a):
            continue
        else:
            return generation_simple_number()
    print(mb_simple_number)
    return mb_simple_number


def gcd_extended(num1, num2):
    if num1 == 0:
        return (num2, 0, 1)
    else:
        div, x, y = gcd_extended(num2 % num1, num1)
    return (div, y - (num2 // num1) * x, x)


def sravnenie_pervoi_ctepeni():
    a = int(input("Введите a: "))
    b = int(input("Введите b: "))
    m = int(input("Введите m: "))
    d, a1, b1 = gcd_extended(a, m)
    if d == 0 or b % d != 0:
        print("Решений нит")
    else:
        m1 = m / d
        mul = b / d
        x = ((a * a1) * mul / a) % m
        for i in range(d):
            print(f"x = {x}(mod{m})")
            x = (x + m1) % m


def sravnenie_vtoroy_ctepeni():
    p = int(input("Введите простое число больше 2: "))
    a = int(input("Введите a: "))
    m = (p - 3) / 4
    g = simbol_iakobi(a, p)
    if g == 0:
        print("x = 0")
    elif g == -1:
        print("Решения нет")
    else:
        x = (a ** (m + 1)) % p
        print(f"x = +/-{x}(mod{p})")


def system_sravneniy():
    array_b = [int(i) for i in input("Введите b через пробел: ").split(" ")]
    array_m = [int(i) for i in input("Введите m через пробел: ").split(" ")]
    M = 1
    for m in array_m:
        M *= m
    array_M = [int(M / i) for i in array_m]
    x = 0
    for i in range(len(array_m)):
        d, a1, b1 = gcd_extended(array_M[i], array_m[i])
        n = a1 % array_m[i]
        x += (array_b[i] * n * array_M[i]) % M
    print(f"x = {x}(mod{M})")


def menu():
    key = int(input("Выберите алгоритм который хотите проверить \n "
                    "1)Расширенный алгоритм Евклида\n "
                    "2)Алгоритм быстрого возведения в степень\n "
                    "3)Алгоритм быстрого возведения в степень по модулю\n "
                    "4)Вычисление символа Якоби\n "
                    "5)Тест Ферма\n "
                    "6)Тест Соловэя-Штрассена\n "
                    "7)Тест Миллера-Рабина\n "
                    "8)Генерация простого числа заданной размерности\n "
                    "9)Решение сравнения первой степени\n "
                    "10)Решение сравнения второй степени\n "
                    "11)Решение системы сравнений\n "
                    "12)Построение конечного поля и реализация операций над данным полем\n "))
    if key == 1:
        Evklide()
    elif key == 2:
        stepen()
    elif key == 3:
        slognai_stepen()
    elif key == 4:
        simbol_iakobi()
    elif key == 5:
        test_ferma()
    elif key == 6:
        test_soloveia()
    elif key == 7:
        test_rabina()
    elif key == 8:
        generation_simple_number()
    elif key == 9:
        sravnenie_pervoi_ctepeni()
    elif key == 10:
        sravnenie_vtoroy_ctepeni()
    elif key == 11:
        system_sravneniy()


def stepen():
    x = 1
    a = int(input("Введите число которое хотите возвести в степень "))
    n = int(input("Введите степень в которую хотите возвести число "))
    b = format(n, "b")
    for i in range(len(b)):
        x = x * pow(a, (int(b[i]) * pow(2, int(i))))

    print(x)


def slognai_stepen():
    a = int(input("Введите число которое хотите возвести в степень "))
    s = int(input("Введите степень в которую хотите возвести число "))
    n = int(input("Введите модуль "))
    b = format(s, "b")
    y = a
    x = pow(a, int(b[0]))
    for i in range(len(b)):
        y = pow(y, 2) % n
        if int(b[i]) == 1:
            x = (x * y) % n

    print(x)


def Evklide():
    x = int(input("введите натуральное число \n x = "))
    y = int(input("Введите натуральное число y удовлетворяющее условию x≥y \n y= "))
    if x < y:
        print("Некоректно введены данные")
        pass
    z = x
    v = y
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
    print(f"НОД(x,y)={m} \n Его линейное представление выглядит {a}*{z}+{b}*{v}={m} ")


if __name__ == "__main__":
    menu()
