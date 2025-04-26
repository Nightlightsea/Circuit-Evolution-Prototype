def logic_and(input_: list) -> float:
    if input_[0] == 1 and input_[1] == 1:
        return 1
    else:
        return 0


def logic_and_switch(input_: list) -> float:
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


def logic_nand(input_: list) -> float:
    if input_[0] == 1 and input_[1] == 1:
        return 0
    else:
        return 1


def logic_nor(input_: list) -> float:
    if input_[0] == 0 and input_[1] == 0:
        return 1
    else:
        return 0


def logic_xnor(input_: list) -> float:
    if input_[0] == input_[1]:
        return 1
    else:
        return 0


def logic_or(input_: list) -> float:
    if input_[0] == 1 or input_[1] == 1:
        return 1
    else:
        return 0


def logic_xor(input_: list) -> float:
    if input_[0] != input_[1]:
        return 1
    else:
        return 0

def logic_not(input_: list) -> float:
    return 1 if input_[0] == 0 else 0


def logic_cable(input_: list) -> float:
    return input_[0]


def logic_plus(input_: list) -> float:
    return input_[0] + input_[1]


def logic_minus(input_: list) -> float:
    return input_[0] - input_[1]


def logic_times(input_: list) -> float:
    return input_[0] * input_[1]


def logic_cap(input_: list) -> float:
    if input_[0] > 0:
        return 1
    return 0


def logic_div(input_: list) -> float:
    if input_[1] != 0:
        return input_[0] / input_[1]
    return 0


def logic_modulo(input_: list) -> float:
    if input_[1] != 0:
        return input_[0] % input_[1]
    else:
        return 0


def pythagoras(input_: list[float]) -> float:
    if input_[0] < 999999 and input_[1] < 999999:
        return (input_[0] ** 2) + (input_[1] ** 2)
    else:
        return 0



# [function, number of inputs, number of outputs]

list_of_logic_gates: list[list]= [
    [logic_and,     2, 1, "and"      ],
    [logic_and_switch,     3, 1, "and-switch"      ],
    [logic_nand,     2, 1, "nand"      ],
    [logic_nor,     2, 1, "nor"      ],
    [logic_xnor,     2, 1, "xnor"      ],
    [logic_or,      2, 1, "or"       ],
    [logic_xor,     2, 1, "xor"       ],
    [logic_not,     1, 1, "not"      ],
    [logic_cable,   1 ,1, "cable"    ],
    [logic_plus,     2, 1, "plus"      ],
    [logic_minus,     2, 1, "minus"      ],
    [logic_times,     2, 1, "times"      ],
    [logic_cap,     1, 1, "cap"      ],
    [logic_div,     2, 1, "div"      ],
    [logic_modulo,     2, 1, "modulo"      ],
    [pythagoras,     2, 1, "pythagoras"      ],
]

