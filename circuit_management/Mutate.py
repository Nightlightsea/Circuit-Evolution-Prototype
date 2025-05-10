import copy
import random

from circuit import CircuitObject
from logic_gates import LogicGates as lg
import settings

config = settings.EvolutionConfig()

def connect(lanes_t, start=0, end=1):
    x = random.randint(start, len(lanes_t) - end)
    y = random.randint(0, len(lanes_t[x]) - 1)
    return [x, y]

def mutate(circuit: CircuitObject.CircuitObjekt, mut=0.1): # TODO: make it so that only one thing can happen at once
    initial_lanes, gates = circuit.__getitem__()
    initial_lanes_t = copy.deepcopy(initial_lanes)
    gates_t = copy.deepcopy(gates)
    mutated = False

    # remove a gate
    if mut > random.randint(0, 100) / 100 or len(gates_t) > config.MAXIMAL_GATE_AMOUNT:
        if len(gates_t) > config.MINIMAL_GATE_AMOUNT:
            to_delete = random.randint(0, len(gates_t) - 1)
            gates_t.remove(gates_t[to_delete])
            mutated = True

    # mutate inputs and outputs
    if mut > random.randint(0, 100) / 100:
        x = random.randint(0, len(gates_t) - 1)
        for i, _ in enumerate(gates_t[x][1]):
            if random.randint(0, 100) > 50:
                gates_t[x][1][i] = connect(initial_lanes_t, end=1)
                mutated = True
        for i, _ in enumerate(gates_t[x][2]):
            if random.randint(0, 100) > 50:
                gates_t[x][2][i] = connect(initial_lanes_t, start=1)
                mutated = True

    # mutate inherent values.
    if mut > random.randint(0, 100) / 100:
        rand_gate = random.randint(0, len(gates_t) - 1)

        # set inherent values
        if gates_t[rand_gate][3]:
            for idx, _ in enumerate(gates_t[rand_gate][3]):
                a = gates_t[rand_gate][3][idx] - round(gates_t[rand_gate][3][idx] * 0.3)
                b = gates_t[rand_gate][3][idx] + round(gates_t[rand_gate][3][idx] * 0.3)
                gates_t[rand_gate][3][idx] = random.randint(a, b) #TODO: have to find a way to find the range of values.

    # TODO: add a way for a gate too mutate into another gate

    # create a new gate
    if mut > random.randint(0, 100) / 100:
        if len(gates_t) <= config.MAXIMAL_GATE_AMOUNT:
            random_gate = lg.list_of_logic_gates[random.randint(0, len(lg.list_of_logic_gates) - 1)]
            gate = [random_gate[0], [], [], []]
            for _ in range(random_gate[1][0]):
                gate[1].append(connect(initial_lanes_t, end=1))
            for _ in range(random_gate[1][1]):
                gate[2].append(connect(initial_lanes_t, start=1))

            # set inherent values
            if random_gate[2]:
                for inherent in random_gate[2]:
                    gate[3].append(random.randint(inherent[0], inherent[1]))

            mutated = True

            # add the new gate
            gates_t.append(gate)

    if mutated:
        circuit_new =  CircuitObject.CircuitObjekt(initial_lanes_t, gates_t)
    else:
        return circuit

    return circuit_new