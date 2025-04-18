from CircuitRun import circuit_run_truth_table


def evaluator(generation, input_output, size_penalty=False):

    best = generation[0]
    y = 0.0
    gen_score_list = []
    for index, g in enumerate(generation):
        gen_score = circuit_run_truth_table(g, input_output)
        gen_score = gen_score - g.get_gate_length() if size_penalty else gen_score
        gen_score_list.append([gen_score, g])
        if gen_score > y:
            best = g
            y = gen_score


    gen_score_sorted = sorted(gen_score_list, key=lambda item: item[0], reverse=True)
    sorte_gen = []
    for gens in gen_score_sorted:
        sorte_gen.append(gens[1])
    return best, y, sorte_gen