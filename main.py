import random

import CircuitObject
import Evaluation
import settings
from CircuitRun import circuit_run_truth_table
from Mutator import create, mutate, crossover

percent_for_size_penalty = 0.80


def build_gen(input_output: list):
    gen_pool_size = settings.GEN_POOL
    mutation_rate = settings.MUTATION_RATE
    generations = settings.GENERATIONS
    population = settings.POPULATION
    number_of_lanes = settings.LANES
    lane_size = settings.LANES_SIZE
    top_p = int(settings.TOP_POPULATION * population)
    best: CircuitObject.CircuitObjekt = create(input_output, lane_num=number_of_lanes, lane_size=lane_size)
    the_very_best = best
    bests_of_gen = []

    # create the initial pool of gen 0
    gen_pool = []
    for _ in range(gen_pool_size):
        gen = [create(input_output, lane_num=number_of_lanes, lane_size=lane_size) for _ in range(population)]
        gen_pool.append(gen)

    size_penalty = False
    for count in range(generations):
        pop = population - 5 if count % 50 == 0 else population

        gen_pool_t = []
        bests_of_gen = []
        gen_bests = []
        for gen in gen_pool:

            best, y, sorted_list = Evaluation.evaluator(gen, input_output, size_penalty)

            #print(f"Generation: {count} Fitness-score: {y}") if count % 10 == 0 else None
            if count % 500 == 0:
                print("________________")
                best.visual()
                print("________________")

            bests = sorted_list[:top_p]
            new_gen = []
            for _ in range(round((pop /2))):
                mutated_random_best = find_random_best_and_mutate(bests, mutation_rate)
                new_gen.append(mutated_random_best)

            for _ in range(round((pop / 2))):
                baby_best = crossover_best(bests)
                baby_best_mutated = mutate(baby_best, mutation_rate)
                new_gen.append(baby_best_mutated)

            bests_of_gen.append((best, y))
            gen_bests.append(best)

            gen_pool_t.append(new_gen)

        if count % 50 <= 1 < count:
            print("------")
            for i in range(len(gen_pool_t)):
                for _ in range(5):
                    baby_best_gen = crossover_best(gen_bests)
                    gen_pool_t[i].append(baby_best_gen)

        print(f"generation {count} fitness score: {list(map(lambda z: z[1], bests_of_gen))}") if count % 1 == 0 else None

        gen_pool = gen_pool_t

        if count >= generations * percent_for_size_penalty or count % 111 <= 1:
            size_penalty = True
            print("Size Penalty activated!") if count == generations * percent_for_size_penalty else None
        else:
            size_penalty = False

    best_score = 0
    for best_g in bests_of_gen:
        if best_g[1] > best_score:
            print(best_g[1])
            best_score = best_g[1]
            the_very_best = best_g[0]

    return the_very_best

def crossover_best(bests):
    random_best_index_1 = random.randint(0, len(bests) - 1)
    random_best_index_2 = random.randint(0, len(bests) - 1)
    random_best_1 = bests[random_best_index_1]
    random_best_2 = bests[random_best_index_2]
    baby = crossover([random_best_1, random_best_2])
    return baby

def find_random_best_and_mutate(bests, mutation):
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
        [[2, 2],  [8]],
        [[3, 3], [18]],
        [[2, 3], [13]],
        [[4, 4], [32]],
        [[4, 2], [20]],
        [[3, 4], [25]],
        [[5, 5], [50]],
        [[5, 2], [29]],
        [[5, 3], [34]],
        [[6, 2], [40]],
        [[5, 1], [26]],
        [[4, 6], [52]],
        [[2, 6], [40]],
        [[1, 5], [26]],
        [[6, 4], [52]],
    ]

    prime = [
        [[2], [3]],
        [[2], [5]],
        [[5], [7]],
        [[7], [11]],
        [[11], [13]],
        [[13], [15]],
        [[15], [17]],
        [[17], [19]],
        [[19], [21]],
        [[21], [23]],
        [[23], [29]],
        [[29], [31]],
        [[31], [37]],
        [[37], [41]],
        [[41], [43]],
             ]

    truth_table = prime

    # run simulation and get the best result
    best_Best = build_gen(truth_table)

    # visualize the best result
    print("_______________________")
    best_Best.visual()
    circuit_run_truth_table(best_Best, truth_table, debug=True)
    print(best_Best.__getitem__()[1])

