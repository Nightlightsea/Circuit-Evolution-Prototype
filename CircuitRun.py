import copy

import CircuitObject
import settings

compute_rounds = settings.COMPUTE_ROUNDS


def circuit_run(circuit: CircuitObject.CircuitObjekt, truth_table, debug=False) -> int:
    initial_lanes, gates = circuit.__getitem__()
    score = 0

    for truth_table_row in truth_table:

        lanes = copy.deepcopy(initial_lanes)
        lanes_next_state = copy.deepcopy(initial_lanes)


        lanes[0] = list(truth_table_row[0])
        for _ in range(compute_rounds):
            for gate in gates:

                # collect the input values to a list.
                con_in = []
                for in_connection in gate[1]:
                    con_in.append(lanes[in_connection[0]][in_connection[1]])

                out = gate[0](con_in)  # Assume gate[0] returns a list/tuple if multiple outputs
                if not isinstance(out, (list, tuple)):  # Ensure output is iterable
                    out = [out]

                for idx, out_connection in enumerate(gate[2]):
                    lanes_next_state[out_connection[0]][out_connection[1]] = out[idx]

            lanes = copy.deepcopy(lanes_next_state)

        score = calculate_score(debug, lanes, score, truth_table_row)

    return  score


def calculate_score(debug, lanes, score, truth_table_row):
    factor = sum([0 if lanes[-1][x] == truth_table_row[1][x] else 1 for x in range(len(lanes[-1]))])
    print(f"got: {lanes[-1]} expected: {[x for x in truth_table_row[1]]} diff: {factor}") if debug else None
    for t_t, check in enumerate(lanes[-1]):
        abs1 = abs(check - truth_table_row[1][t_t]) * factor
        score += (1 / abs1) if abs1 != 0 else 0
    return score * 1000

#score - (len(gates)) #* (((20 + 1) / (len(gates) + 1)) - 1)
#if check == truth_table_row[1][t_t]:
#    score += 90
#elif score > 100:
#    score -= 100