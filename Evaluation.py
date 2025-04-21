import CircuitObject
from CircuitRun import circuit_run_truth_table


def evaluator(generation: list[CircuitObject.CircuitObjekt], gen_num, input_output, size_penalty=False):

    best = generation[0]
    best_score = float('inf')
    gen_score_list = []
    for index, g in enumerate(generation):
        if g.get_last_change() >= gen_num:
            g.set_score(circuit_run_truth_table(g, input_output), gen_num)

        gen_score = g.get_score() + g.get_gate_length() if size_penalty else g.get_score()

        gen_score_list.append([gen_score, g])
        if gen_score < best_score:
            best = g
            best_score = gen_score


    gen_score_sorted = sorted(gen_score_list, key=lambda item: item[0])
    sorted_gen = []
    for gens in gen_score_sorted:
        sorted_gen.append(gens[1])

    return best, best_score, sorted_gen