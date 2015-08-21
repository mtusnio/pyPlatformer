__author__ = 'Maverick'


def sign(number):
    return (1, -1)[number < 0]


def bits(n):
    while n:
        b = n & (~n+1)
        yield b
        n ^= b


def clamp(val, min, max):
    if min > max:
        raise ValueError

    return sorted([min, val, max])[1]
