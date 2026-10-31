import copy
import random

from circuit import CircuitObject
from circuit_management.ConnectGate import connect
from circuit_management.CreateReplaceGate import create_or_replace_gate
import settings

config = settings.EvolutionConfig()


def mutate(circuit: CircuitObject.CircuitObjekt,
           mut=0.1) -> CircuitObject.CircuitObjekt:
    initial_lanes, gates = circuit.__getitem__()
    initial_lanes_copy = copy.deepcopy(initial_lanes)
    gates_copy = copy.deepcopy(gates)
    mutated = False
    changes = 2

    for _ in range(changes):
        if mut > random.randint(0, 100) / 100:
            random_mutation = random.randint(1, 5)
            mutated = True
            match random_mutation:
                case 1:  # remove a gate.
                    if len(gates_copy) > config.MINIMAL_GATE_AMOUNT:
                        remove_gate(gates_copy)
                case 2:  #mutate inputs and outputs.
                    mutate_in_and_outputs(gates_copy, initial_lanes_copy)
                case 3:  # mutate inherent values.
                    mutate_inherent_values(gates_copy)
                case 4:  # replace a gate.
                    replace_gate(gates_copy, initial_lanes_copy)
                case 5:  # create a new gate.
                    if len(gates_copy) <= config.MAXIMAL_GATE_AMOUNT:
                        gates_copy.append(create_or_replace_gate(initial_lanes_copy))

    # remove gates if there are too many.
    while len(gates_copy) > config.MAXIMAL_GATE_AMOUNT:
        remove_gate(gates_copy)
        mutated = True

    if mutated:
        circuit_new = CircuitObject.CircuitObjekt(initial_lanes_copy, gates_copy)
    else:
        return circuit

    return circuit_new


def remove_gate(gates_t):
    if len(gates_t) > config.MINIMAL_GATE_AMOUNT:
        to_delete = random.randint(0, len(gates_t) - 1)
        gates_t.remove(gates_t[to_delete])


def replace_gate(gates_t, initial_lanes_t):
    gate_choice = random.randint(0, len(gates_t) - 1)
    selected_gate = gates_t[gate_choice]
    replacement_gate = create_or_replace_gate(initial_lanes_t, selected_gate[1], selected_gate[2])
    gates_t[gate_choice] = replacement_gate


def mutate_inherent_values(gates_t):
    rand_gate = random.randint(0, len(gates_t) - 1)
    # set inherent values
    if gates_t[rand_gate][3]:
        for idx, _ in enumerate(gates_t[rand_gate][3]):
            a = gates_t[rand_gate][3][idx] - round(gates_t[rand_gate][3][idx] * 0.1)
            b = gates_t[rand_gate][3][idx] + round(gates_t[rand_gate][3][idx] * 0.1)
            gates_t[rand_gate][3][idx] = random.randint(a, b)  # TODO: have to find a way to find the range of values.


def mutate_in_and_outputs(gates_t, initial_lanes_t):
    x = random.randint(0, len(gates_t) - 1)
    for i, _ in enumerate(gates_t[x][1]):
            gates_t[x][1][i] = connect(initial_lanes_t, end=1)
    for i, _ in enumerate(gates_t[x][2]):
            gates_t[x][2][i] = connect(initial_lanes_t, start=1)
