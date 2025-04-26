import copy

import CircuitObject
import settings

config = settings.EvolutionConfig()

def circuit_run_truth_table(circuit: CircuitObject.CircuitObjekt, truth_table, debug=False) -> int:
    initial_lanes, gates = circuit.__getitem__()
    score = 0
    stab = 0

    for truth_table_row in truth_table:

        output_lanes, stab = execute_circuit(gates, initial_lanes, truth_table_row)
        score += calculate_score(debug, output_lanes, truth_table_row)

    if stab < round(config.COMPUTE_ROUNDS / 2):
        score *= 2

    return  score * 100


def execute_circuit(gates, initial_lanes: list[list], truth_table_row: list[list]):
    lanes = copy.deepcopy(initial_lanes)
    lanes[0] = list(truth_table_row[0]) # input lanes
    lanes_next_state = copy.deepcopy(lanes)
    check_if_stabilized = lanes[-1].copy()
    stabilized = 0

    for _ in range(config.COMPUTE_ROUNDS):
        lanes = run_once(gates, lanes, lanes_next_state)
        if lanes[-1] == check_if_stabilized:
            stabilized += 1
        else:
            stabilized = 0
        check_if_stabilized = lanes[-1].copy()

    return lanes, stabilized


def run_once(gates, lanes, lanes_next_state):

    for gate in gates:

        # collect the input values to a list.
        con_in = []
        for in_connection in gate[1]:
            con_in.append(lanes[in_connection[0]][in_connection[1]])

        try:
            out = gate[0](con_in)  # Assume gate[0] returns a list/tuple if multiple outputs
        except ValueError as e:
            print(f"Error: {e}")
            out = 0
        if not isinstance(out, (list, tuple)):  # Ensure output is iterable
            out = [out]

        for idx, out_connection in enumerate(gate[2]):
            lanes_next_state[out_connection[0]][out_connection[1]] = out[idx]

    lanes = copy.deepcopy(lanes_next_state)

    return lanes


def calculate_score(debug, lanes, truth_table_row):
    scores: float = 0
    factor: float = sum([0 if lanes[-1][x] == truth_table_row[1][x] else 1 for x in range(len(lanes[-1]))])

    print(f"got: {lanes[-1]} expected: {[x for x in truth_table_row[1]]} diff: {factor}") if debug else None

    for t_t, check in enumerate(lanes[-1]):
        abs1: float = abs(check - truth_table_row[1][t_t])
        #abs1 = 1 if abs1 == 0 else abs1
        #abs1 = 100 * (abs1 / abs1 + 10 ) + (factor * 10)
        scores += abs1 * abs1 * factor #* (factor*10)
    return scores
