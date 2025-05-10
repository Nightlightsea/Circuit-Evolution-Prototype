def logic_and(input_: list, *argv) -> float:
    if input_[0] == 1 and input_[1] == 1:
        return 1
    else:
        return 0


def logic_and_switch(input_: list, *argv) -> float:
    if input_[2] == 1:
        if input_[0] == 1 and input_[1] == 1:
            return 1
        else:
            return 0
    else:
        if input_[0] == 1 or input_[1] == 1:
            return 1
        else:
            return 0


def logic_nand(input_: list, *argv) -> float:
    if input_[0] == 1 and input_[1] == 1:
        return 0
    else:
        return 1


def logic_nor(input_: list, *argv) -> float:
    if input_[0] == 0 and input_[1] == 0:
        return 1
    else:
        return 0


def logic_xnor(input_: list, *argv) -> float:
    if input_[0] == input_[1]:
        return 1
    else:
        return 0


def logic_or(input_: list, *argv) -> float:
    if input_[0] == 1 or input_[1] == 1:
        return 1
    else:
        return 0


def logic_xor(input_: list, *argv) -> float:
    if input_[0] != input_[1]:
        return 1
    else:
        return 0


def logic_not(input_: list, *argv) -> float:
    return 1 if input_[0] == 0 else 0


def logic_cable(input_: list, *argv) -> float:
    return input_[0]


def logic_always_1(input_: list, *argv) -> float:
    return 1


def logic_always_0(input_: list, *argv) -> float:
    return 0
