import random

from circuit import CircuitObject
from logic_gates import LogicGates as lg
from circuit_management.Mutate import config, connect


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
