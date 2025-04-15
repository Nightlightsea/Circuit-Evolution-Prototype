import copy
import random

import CircuitObject
import LogicGates as lg


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
    for _ in range(2):
        gate_list.append(lg.list_of_logic_gates[random.randint(0, len(lg.list_of_logic_gates) - 1)])

    gate_connect = []
    for gate in gate_list:
        gate_connect.append([gate[0], [], []])
        for _ in range(gate[1]):
            gate_connect[-1][1].append(connect(lanes, end=2))
        for _ in range(gate[2]):
            gate_connect[-1][2].append(connect(lanes, start=1))

    circuit_full = CircuitObject.CircuitObjekt(lanes, gate_connect)

    return circuit_full


def mutate(circuit: CircuitObject.CircuitObjekt, mut=0.1):
    initial_lanes, gates = circuit.__getitem__()
    initial_lanes_t = copy.deepcopy(initial_lanes)
    gates_t = copy.deepcopy(gates)

    # remove a gate
    if mut > random.randint(0, 100) / 100:
        if len(gates_t) > 1:
            to_delete = random.randint(0, len(gates_t) - 1)
            gates_t.remove(gates_t[to_delete])

    # mutate inputs and outputs
    if mut > random.randint(0, 100) / 100:
        x = random.randint(0, len(gates_t) - 1)
        for i, _ in enumerate(gates_t[x][1]):
            if random.randint(0, 100) > 50:
                gates_t[x][1][i] = connect(initial_lanes_t, end=2)
        for i, _ in enumerate(gates_t[x][2]):
            if random.randint(0, 100) > 50:
                gates_t[x][2][i] = connect(initial_lanes_t, start=1)

    # create a new gate
    if mut > random.randint(0, 100) / 100:
        random_gate = lg.list_of_logic_gates[random.randint(0, len(lg.list_of_logic_gates) - 1)]
        gate = [random_gate[0], [], []]
        for _ in range(random_gate[1]):
            gate[1].append(connect(initial_lanes_t, end=2))
        for _ in range(random_gate[2]):
            gate[2].append(connect(initial_lanes_t, start=1))
        # add the new gate
        gates_t.append(gate)

    circuit_new =  CircuitObject.CircuitObjekt(initial_lanes_t, gates_t)

    return circuit_new


def crossover(circuits: list[CircuitObject.CircuitObjekt]):
    circ_gates = []
    running = True
    lanes = copy.deepcopy(circuits[0].__getitem__()[0])
    selected_gates = []

    for cir in circuits:
        circ_gates.append(copy.deepcopy(cir.__getitem__()[1]))

    gates_row = 0
    while running:
        running = False

        gate_to_select = []
        for gates_column in circ_gates:

            if gates_row < len(gates_column):
                gate_to_select.append(gates_column[gates_row])
                running = True

        if len(gate_to_select) > 1:
            selected_gates.append(gate_to_select[random.randint(0, len(gate_to_select) - 1)])
        elif 50 > random.randint(0, 100) and running:
            selected_gates.append(gate_to_select[0])

        gates_row += 1

    new_circuit = CircuitObject.CircuitObjekt(lanes, selected_gates)

    return new_circuit