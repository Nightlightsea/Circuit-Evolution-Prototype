from logic_gates.BinaryGates import *
from logic_gates.MathGates import *

# [function, [inputs, outputs], [[min number, max number], ... ]](inherent values, optional.), "name of gate"]
list_of_logic_gates: list[list]= [
    [logic_and, [2, 1], [], "and"],
    #[logic_and_switch, [3, 1], [], "and-switch"],
    [logic_nand, [2, 1], [], "nand"],
    [logic_nor, [2, 1], [], "nor"],
    [logic_xnor, [2, 1], [], "xnor"],
    [logic_or, [2, 1], [], "or"],
    [logic_xor, [2, 1], [], "xor"],
    [logic_not, [1, 1], [], "not"],
    [logic_cable, [1 , 1], [], "cable"],
    [logic_always_1, [0, 1], [], "always 1"],
    [logic_always_0, [0, 1], [], "always 0"],
    #[logic_always_2, [1, 1], [], "always 2"],
    #[logic_random_int, [0, 1], [[0, 100]], "Int"],
    #[logic_always_pi, [1, 1], [], "Pi"],
    #[logic_plus, [2, 1], [], "plus"],
    #[logic_minus, [2, 1], [], "minus"],
    #[logic_times, [2, 1], [], "times"],
    #[logic_cap, [1, 1], [], "cap"],
    #[logic_div, [2, 1], [], "div"],
    #[logic_root, [1, 1], [], "root"],
    #[logic_modulo, [2, 1], [], "modulo"],
    #[gate_biggest, [2, 1], [], "biggest"],
    #[pythagoras, [2, 1], [], "pythagoras"],
    #[two_plus_1_minus, [3, 1], [], "pythagoras"],
]


