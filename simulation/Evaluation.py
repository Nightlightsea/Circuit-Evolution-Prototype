from circuit import CircuitObject
import settings
from circuit.CircuitObject import CircuitObjekt
from circuit.RunCircuit import execute_circuit

config = settings.EvolutionConfig()


def evaluator(species: list[int | list[CircuitObject.CircuitObjekt]], gen_num, input_output, size_penalty=False) -> \
tuple[CircuitObjekt, float, list[int | list[CircuitObjekt]]]:

    best = species[1][0]
    best_score = float('inf')
    specie_score_list = []
    specie_id = species[0]
    specie = species[1]
    for index, circuit in enumerate(specie):
        if circuit.get_last_change() >= gen_num: # if it's a new circuit, compute it's score.
            circuit.set_score(circuit_run_truth_table(circuit, input_output), gen_num)

        # If the gate penalty is activated, add the number of gates to the score.
        specie_score: float = circuit.get_score() + circuit.get_gate_length() if size_penalty else circuit.get_score()

        specie_score_list.append([specie_score, circuit])
        if specie_score < best_score:
            best = circuit
            best_score = specie_score

    specie_score_sorted: list[list] = sorted(specie_score_list, key=lambda item: item[0])
    specie_sorted: list[int | list[CircuitObject.CircuitObjekt]] = [specie_id, []]
    for gens in specie_score_sorted:
        specie_sorted[1].append(gens[1])

    return best, best_score, specie_sorted


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
