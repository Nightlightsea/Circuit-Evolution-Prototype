import copy
import random

from circuit import CircuitObject


def crossover(circuits: list[CircuitObject.CircuitObjekt]):
    lanes = copy.deepcopy(circuits[0].__getitem__()[0])

    # get the gates of every circuit, and put them in the list based on order.
    circ_gates = []
    count_gates_per_circuit = []
    for i, circuit in enumerate(circuits):
        gates = circuit.__getitem__()[1]
        count_gates_per_circuit.append(len(gates))
        for g, gate in enumerate(gates):
            if len(circ_gates) - 1 < g:
                circ_gates.append([])
            circ_gates[g].append(gate)


    # Set the final amount of gates in the new circuit somewhere between the min and max amount of gates of the parent circuits.
    final_amount_of_gates = random.randint(min(count_gates_per_circuit), max(count_gates_per_circuit))

    # TODO: make inherent values crossover too if possible.

    # select the gates for the new circuit
    selected_gates = []
    for count, gate_choice in enumerate(circ_gates):
        selected_gates.append(gate_choice[random.randint(0, len(gate_choice) - 1)])
        if  count >= final_amount_of_gates:
            break

    new_circuit = CircuitObject.CircuitObjekt(lanes, selected_gates)

    return new_circuit
