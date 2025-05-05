import copy
import random

import CircuitObject
import LogicGates as lg
import settings

config = settings.EvolutionConfig()


def connect(lanes_t, start=0, end=1):
    x = random.randint(start, len(lanes_t) - end)
    y = random.randint(0, len(lanes_t[x]) - 1)
    return [x, y]


def create(in_out: list, lane_num=2, lane_size=4):

    lanes = [[0 for _ in range(len(in_out[0][0]))]]
    for _ in range(lane_num):
        lanes.append([])
        for _ in range(lane_size):
            lanes[-1].append(0)
    lanes.append([])
    for _ in range(len(in_out[0][1])):
        lanes[-1].append(0)

    gate_list = []
    for _ in range(config.INITIAL_GATE_AMOUNT):
        gate_list.append(lg.list_of_logic_gates[random.randint(0, len(lg.list_of_logic_gates) - 1)])

    gate_connect = []
    for gate in gate_list:
        gate_connect.append([gate[0], [], [], []]) #TODO: make a new gate instead of appending it directly.
        for _ in range(gate[1][0]):
            gate_connect[-1][1].append(connect(lanes, end=1))
        for _ in range(gate[1][1]):
            gate_connect[-1][2].append(connect(lanes, start=1))

        # set inherent values
        if gate[2]:
            for inherent in gate[2]:
                gate_connect[-1][3].append(random.randint(inherent[0], inherent[1]))

    circuit_full = CircuitObject.CircuitObjekt(lanes, gate_connect)

    return circuit_full


def mutate(circuit: CircuitObject.CircuitObjekt, mut=0.1):
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


def crossover(circuits: list[CircuitObject.CircuitObjekt]): #TODO: needs rewrite to make it more understandable.
    circ_gates = []
    running = True
    lanes = copy.deepcopy(circuits[0].__getitem__()[0])
    selected_gates = []

    for cir in circuits:
        circ_gates.append(copy.deepcopy(cir.__getitem__()[1]))

    number_of_selected_gates = 0
    gates_row = 0
    while running:
        running = False

        gate_to_select = []
        for gates_column in circ_gates:

            if gates_row < len(gates_column) and gates_row <= config.MAXIMAL_GATE_AMOUNT:
                gate_to_select.append(gates_column[gates_row])
                running = True

        if number_of_selected_gates < config.MAXIMAL_GATE_AMOUNT:
            if len(gate_to_select) > 1:
                if random.randint(0, 100) > 20:
                    for gate in gate_to_select:
                        selected_gates.append(gate)
                        number_of_selected_gates += 1
                else:
                    selected_gates.append(gate_to_select[random.randint(0, len(gate_to_select) - 1)])
                    number_of_selected_gates += 1
            elif 50 > random.randint(0, 100) and running:
                selected_gates.append(gate_to_select[0])
                number_of_selected_gates += 1

        gates_row += 1

    new_circuit = CircuitObject.CircuitObjekt(lanes, selected_gates)

    return new_circuit