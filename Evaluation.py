import CircuitObject
import settings
from CircuitRun import execute_circuit

config = settings.EvolutionConfig()

def evaluator(species: list[CircuitObject.CircuitObjekt], gen_num, input_output, size_penalty=False):

    best = species[0]
    worst_score = float('inf')
    gen_score_list = []
    for index, circuit in enumerate(species):
        if circuit.get_last_change() >= gen_num:
            circuit.set_score(circuit_run_truth_table(circuit, input_output), gen_num)
        gen_score: float = circuit.get_score() + circuit.get_gate_length() if size_penalty else circuit.get_score()

        gen_score_list.append([gen_score, circuit])
        if gen_score < worst_score:
            best = circuit
            worst_score = gen_score

    gen_score_sorted: list[list] = sorted(gen_score_list, key=lambda item: item[0])
    sorted_gen: list[CircuitObject.CircuitObjekt] = []
    for gens in gen_score_sorted:
        sorted_gen.append(gens[1])

    return best, worst_score, sorted_gen

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
