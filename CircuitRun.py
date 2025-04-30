import copy

import CircuitObject
import settings

config = settings.EvolutionConfig()


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


