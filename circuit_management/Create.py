import random

from circuit import CircuitObject
from circuit_management.CreateReplaceGate import create_or_replace_gate
from circuit_management.Mutate import config


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
        gate_list.append(create_or_replace_gate(lanes))

    circuit_full = CircuitObject.CircuitObjekt(lanes, gate_list)

    return circuit_full
