def logic_and(input_: list) -> int:
    if input_[0] == input_[1]:
        return 1
    else:
        return 0


def logic_or(input_: list) -> int:
    if input_[0] == 1 or input_[1] == 1:
        return 1
    else:
        return 0

def logic_xor(input_: list) -> int:
    if input_[0] == 1 or input_[1] == 1:
        if input_[0] == 0 or input_[1] == 0:
            return 1
    return 0


def logic_not(input_: list) -> int:
    return 1 if input_[0] == 0 else 0


def logic_cable(input_: list) -> int:
    return input_[0]


def logic_plus(input_: list) -> int:
    return input_[0] + input_[1]


def logic_minus(input_: list) -> int:
    return input_[0] - input_[1]


def logic_times(input_: list) -> int:
    return input_[0] * input_[1]


def logic_div(input_: list) -> float:
    if input_[0] > 0 and input_[1] > 0:
        return input_[0] / input_[1]
    return 0

# [function, number of inputs, number of outputs]

list_of_logic_gates = [
    [logic_and,     2, 1, "and"      ],
    [logic_or,      2, 1, "or"       ],
    [logic_xor,     2, 1, "xor"       ],
    [logic_not,     1, 1, "not"      ],
    [logic_cable,   1 ,1, "cable"    ],
    [logic_plus,     2, 1, "plus"      ],
    [logic_minus,     2, 1, "minus"      ],
    [logic_times,     2, 1, "times"      ],
    [logic_div,     2, 1, "div"      ],
]

