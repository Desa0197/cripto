from random import randint


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
