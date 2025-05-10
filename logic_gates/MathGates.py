import math


def logic_random_int(input_: list, value) -> float:
    return value[0]


def logic_always_pi(*argv) -> float:
    return math.pi


def logic_plus(input_: list, *argv) -> float:
    return input_[0] + input_[1]


def logic_minus(input_: list, *argv) -> float:
    return input_[0] - input_[1]


def logic_times(input_: list, *argv) -> float:
    return input_[0] * input_[1]


def logic_cap(input_: list, *argv) -> float:
    if input_[0] > 0:
        return 1
    return 0


def logic_div(input_: list, *argv) -> float:
    if input_[0] < 99999 and input_[1] < 99999:
        if input_[1] != 0:
            return input_[0] / input_[1]
    return 0


def logic_root(input_: list, *argv) -> float:
    if input_[0] < 99999:
        if input_[0] > 0:
            x = math.sqrt(input_[0])
        else:
            x = 0
        return x
    return 0


def logic_modulo(input_: list, *argv) -> float:
    if input_[1] != 0:
        return input_[0] % input_[1]
    else:
        return 0


def pythagoras(input_: list[float], *argv) -> float:
    if -9999 < input_[0] < 9999 and -9999 < input_[1] < 9999:
        return (input_[0] ** 2) + (input_[1] ** 2)
    else:
        return 0


def logic_always_2(input_: list, *argv) -> float:
    return 2
