import random

from circuit_management.ConnectGate import connect
from logic_gates import LogicGates as lg


def create_or_replace_gate(lanes: list[list], inputs: list=None, outputs: list=None) -> list:
    prev_gate_input_length: int = len(inputs) if inputs is not None else 0
    prev_gate_output_length: int = len(outputs) if outputs is not None else 0

    # ---first create a random empty gate--- #
    # get random gate from gate list and create new empty gate from it.
    new_gate_template = lg.list_of_logic_gates[random.randint(0, len(lg.list_of_logic_gates) - 1)]
    new_gate = [new_gate_template[0], [], [], []]
    # get in/output length from the new gate.
    new_gate_input_length: int = new_gate_template[1][0]
    new_gate_output_length: int = new_gate_template[1][1]

    # ---populate the in/outputs with previous in/outputs if they exist.--- #
    # populate inputs
    for i in range(prev_gate_input_length):
        if i <= new_gate_input_length:
            new_gate[1].append(inputs[i])
    # populate outputs
    for i in range(prev_gate_output_length):
        if i <= new_gate_output_length:
            new_gate[2].append(outputs[i])

    # ---populate all not yet used in/outputs--- #
    unused_input: int = new_gate_input_length - len(new_gate[1])
    unused_output: int = new_gate_output_length - len(new_gate[2])
    # populate inputs.
    for i in range(unused_input):
        new_gate[1].append(connect(lanes, end=1))
    # populate outputs.
    for i in range(unused_output):
        new_gate[2].append(connect(lanes, start=1))

    # ---set inherent values--- #
    if new_gate_template[2]:
        for inherent in new_gate_template[2]:
            new_gate[3].append(random.randint(inherent[0], inherent[1]))

    return new_gate
