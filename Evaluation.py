import CircuitObject
from CircuitRun import circuit_run_truth_table


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