import multiprocessing
import random
import time
from functools import partial

import CircuitObject
import CircuitRun
import Evaluation
import settings
from Mutator import create, mutate, crossover

config = settings.EvolutionConfig()


def worker_evo(specie, gen: int, inout: list[list], penalty: float):
    best, score, score_list = Evaluation.evaluator(specie, gen, inout, penalty)
    return best, score, score_list


def run_simulation(input_output: list) -> CircuitObject.CircuitObjekt:
    top_p = int(config.TOP_POPULATION * config.POPULATION)

    bests_of_generation_with_score = []
    # create the initial pool of gen 0
    gene_pool = []

    for _ in range(config.GEN_POOL):
        species = [create(input_output, lane_num=config.LANES, lane_size=config.LANES_SIZE) for _ in range(config.POPULATION)]
        gene_pool.append(species)

    start: float = time.time()
    size_penalty = False
    for current_generation in range(config.GENERATIONS):


        gene_pool_next: list[list] = []
        bests_of_generation_with_score = []


        #-----Multithreading-----#
        worker = partial(worker_evo, gen=current_generation, inout=input_output, penalty=size_penalty)
        if config.MULTITHREADING:
            with multiprocessing.Pool(processes=config.CORES) as process_pool:
                result = process_pool.map(worker, gene_pool)
        else:
            result = map(worker, gene_pool)

        # ------------------------------ #
        for the_best_of_the_species, score_of_circuit, species_score_list in result:
            population_size: int = config.POPULATION


            if current_generation % 200 == 0:
                print("________________")
                the_best_of_the_species.visual()
                CircuitRun.circuit_run_truth_table(the_best_of_the_species, input_output, debug=True)
                print("________________")

            #----Prepare the next generation.----#
            top_bests_of_the_species = species_score_list[:top_p].copy()
            next_generation_of_species = []
            next_generation_of_species.extend(top_bests_of_the_species)

            population_size -= len(top_bests_of_the_species)
            create_new_circuits(top_bests_of_the_species, next_generation_of_species, population_size)

            bests_of_generation_with_score.append((the_best_of_the_species, score_of_circuit))
            gene_pool_next.append(next_generation_of_species)
        # ------------------------------ #

        time_taken: float = time.time() - start

        # crossover between gens, still needs improvements because it's too random right now.
        if current_generation % config.GENERATION_CROSSOVER <= config.GENERATION_CROSSOVER_DURATION < current_generation:
            print("------")
            for i in range(len(gene_pool_next)):
                for _ in range(config.CROSSOVER_IN_GEN):
                    baby_best_gen = crossover([bests_of_generation_with_score[i][0], bests_of_generation_with_score[random.randint(0, len(gene_pool_next) - 1)][0]])
                    gene_pool_next[i].append(baby_best_gen)

        # removing a species if they are worse than the best by a factor.
        if current_generation % 20 == 0 < current_generation:
            replace_worst_species_in_pool(bests_of_generation_with_score, gene_pool_next, current_generation, input_output)

        time_estimate = (time_taken / (current_generation + 1)) * (config.GENERATIONS - current_generation)
        minutes = time_estimate / 60
        seconds = time_estimate % 60
        print(f"generation: {current_generation} time estimate: {minutes:.0f}:{round(seconds)} fitness score: {list(map(lambda z: z[1], bests_of_generation_with_score))}") if current_generation % 1 == 0 else None

        gene_pool = gene_pool_next

        if current_generation >= config.GENERATIONS * config.PENALTY: #  or time_taken > 0.5 or 0 <= count_down < 10:
            size_penalty = True
            print("Size Penalty activated!") if current_generation == config.GENERATIONS * config.PENALTY else None
        else:
            size_penalty = False


    the_very_best = sorted(bests_of_generation_with_score, key=lambda item: item[1])[0]

    return the_very_best[0]


def create_new_circuits(bests, new_gen, pop):
    for _ in range(round((pop / 2))):
        mutated_random_best = find_random_best_and_mutate(bests, config.MUTATION_RATE)
        new_gen.append(mutated_random_best)
    for _ in range(round((pop / 2))):
        baby_best = crossover_best(bests)
        baby_best_mutated = mutate(baby_best, config.MUTATION_RATE)
        new_gen.append(baby_best_mutated)


def select_parents():
    return


def replace_worst_species_in_pool(bests_of_gen, gen_pool_t, generations_count, input_output):
    num_species = len(bests_of_gen)
    if num_species < 2:
        # Need at least two species to compare and potentially remove one
        return

    scores              = [circ[1] for circ in bests_of_gen]
    bests               = [best_c[0] for best_c in bests_of_gen]
    best_score          = min(scores)
    worst_check_select  = -1
    worst: float        = 0
    max_removal         = 2
    removed             = 0
    for i, worst_for_check in enumerate(bests_of_gen):
        if worst < worst_for_check[1] > best_score * 1.4 and i < len(bests_of_gen) * 0.7:
            worst_check_select = i
            worst = worst_for_check[1]


    if worst_check_select > -1:
        print(f"Removing: {worst_check_select} with a score of {bests_of_gen[worst_check_select][1]}")
        new_species = []
        at_random_crossover_mutation_creation = random.randint(1, 3)

        if at_random_crossover_mutation_creation == 1:
            new_species.extend([crossover_best(bests) for _ in
                           range(config.POPULATION)])

        if at_random_crossover_mutation_creation == 2:
            create_new_circuits(bests, new_species, config.POPULATION)

        if at_random_crossover_mutation_creation == 3:
            new_species.extend([create(input_output, lane_num=config.LANES, lane_size=config.LANES_SIZE) for _ in
                                range(round(config.POPULATION))])
        gen_pool_t.remove(gen_pool_t[worst_check_select])
        gen_pool_t.append(new_species)




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