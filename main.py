import random

import Evaluation
import settings
from CircuitRun import circuit_run
from Mutator import create, mutate

percent_for_size_penalty = 0.75


def build_gen(input_output: list):
    mutation_rate = settings.MUTATION_RATE
    generations = settings.GENERATIONS
    population = settings.POPULATION
    number_of_lanes = settings.LANES
    lane_size = settings.LANES_SIZE
    top_p = int(settings.TOP_POPULATION * population)
    best = None


    # create the initial pool of gen 0
    gen = [create(input_output, lane_num=number_of_lanes, lane_size=lane_size) for _ in range(population)]

    size_penalty = False
    for count in range(generations):

        best, y, sorted_list = Evaluation.evaluator(gen, input_output, size_penalty)

        print(f"Generation: {count} Fitness-score: {y}") if count % 50 == 0 else None
        best.visual() if count % 410 == 0 else None

        bests = sorted_list[:top_p]
        new_gen = []
        for n_g in range(round(population/2)):
            mutated_random_best = find_random_best(bests, mutation_rate)
            new_gen.append(mutated_random_best)
        new_gen += [create(input_output) for _ in range(round(population/2))]
        gen = new_gen

        if count >= generations * percent_for_size_penalty:
            size_penalty = True
            print("Size Penalty activated!") if count == generations * percent_for_size_penalty else None
        else:
            size_penalty = False

    return best


def find_random_best(bests, mutation):
    random_best_index = random.randint(0, len(bests) - 1)
    random_best = bests[random_best_index]
    mutated_random_best = mutate(random_best, mut=mutation)
    return mutated_random_best


if __name__ == '__main__':

    in_out = [
        [[1, 0, 1, 0], [1, 0, 0, 0]],
        [[1, 0, 0, 0], [0, 0, 0, 1]],
        [[0, 0, 0, 0], [1, 0, 0, 0]],
        [[0, 0, 1, 0], [0, 0, 0, 1]],
        [[0, 1, 0, 0], [1, 0, 0, 0]]
    ]
    truth_table_full_adder_3_in_2_out = [
        [[0, 0, 0], [0, 0]],  # 0 + 0 + 0 = 0, Cout = 0
        [[0, 0, 1], [1, 0]],  # 0 + 0 + 1 = 1, Cout = 0
        [[0, 1, 0], [1, 0]],  # 0 + 1 + 0 = 1, Cout = 0
        [[0, 1, 1], [0, 1]],  # 0 + 1 + 1 = 0, Cout = 1
        [[1, 0, 0], [1, 0]],  # 1 + 0 + 0 = 1, Cout = 0
        [[1, 0, 1], [0, 1]],  # 1 + 0 + 1 = 0, Cout = 1
        [[1, 1, 0], [0, 1]],  # 1 + 1 + 0 = 0, Cout = 1
        [[1, 1, 1], [1, 1]],  # 1 + 1 + 1 = 1, Cout = 1
    ]

    truth_table_4_in_4_out_logic1 = [
        [[0, 0, 0, 0], [0, 0, 0, 1]],  # In: 0000, Out: 0^0=0, 0&0=0, 0|0=0, !0=1
        [[0, 0, 0, 1], [0, 0, 1, 1]],  # In: 0001, Out: 0^0=0, 0&0=0, 0|1=1, !0=1
        [[0, 0, 1, 0], [0, 0, 1, 1]],  # In: 0010, Out: 0^0=0, 0&1=0, 1|0=1, !0=1
        [[0, 0, 1, 1], [0, 0, 1, 1]],  # In: 0011, Out: 0^0=0, 0&1=0, 1|1=1, !0=1
        [[0, 1, 0, 0], [1, 0, 0, 1]],  # In: 0100, Out: 0^1=1, 1&0=0, 0|0=0, !0=1
        [[0, 1, 0, 1], [1, 0, 1, 1]],  # In: 0101, Out: 0^1=1, 1&0=0, 0|1=1, !0=1
        [[0, 1, 1, 0], [1, 1, 1, 1]],  # In: 0110, Out: 0^1=1, 1&1=1, 1|0=1, !0=1
        [[0, 1, 1, 1], [1, 1, 1, 1]],  # In: 0111, Out: 0^1=1, 1&1=1, 1|1=1, !0=1
        [[1, 0, 0, 0], [1, 0, 0, 0]],  # In: 1000, Out: 1^0=1, 0&0=0, 0|0=0, !1=0
        [[1, 0, 0, 1], [1, 0, 1, 0]],  # In: 1001, Out: 1^0=1, 0&0=0, 0|1=1, !1=0
        [[1, 0, 1, 0], [1, 0, 1, 0]],  # In: 1010, Out: 1^0=1, 0&1=0, 1|0=1, !1=0
        [[1, 0, 1, 1], [1, 0, 1, 0]],  # In: 1011, Out: 1^0=1, 0&1=0, 1|1=1, !1=0
        [[1, 1, 0, 0], [0, 0, 0, 0]],  # In: 1100, Out: 1^1=0, 1&0=0, 0|0=0, !1=0
        [[1, 1, 0, 1], [0, 0, 1, 0]],  # In: 1101, Out: 1^1=0, 1&0=0, 0|1=1, !1=0
        [[1, 1, 1, 0], [0, 1, 1, 0]],  # In: 1110, Out: 1^1=0, 1&1=1, 1|0=1, !1=0
        [[1, 1, 1, 1], [0, 1, 1, 0]],  # In: 1111, Out: 1^1=0, 1&1=1, 1|1=1, !1=0
    ]

    x = [
        [[2,2],  [8]],
        [[3, 3], [18]],
        [[2, 3], [13]],
        [[4, 4], [32]],
        [[4, 2], [20]],
        [[3, 4], [25]]
    ]

    truth_table = x

    # run simulation and get the best result
    best_Best = build_gen(truth_table)

    # visualize the best result
    best_Best.visual()
    circuit_run(best_Best, truth_table, debug=True)
    print(best_Best.__getitem__()[1])

