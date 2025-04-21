import random
import time

import CircuitObject
import CircuitRun
import Evaluation
import settings
from Mutator import create, mutate, crossover

config = settings.EvolutionConfig()

def build_gen(input_output: list):
    top_p = int(config.TOP_POPULATION * config.POPULATION)
    the_best_of_the_species: CircuitObject.CircuitObjekt = create(input_output, lane_num=config.LANES, lane_size=config.LANES_SIZE)
    the_very_best = the_best_of_the_species
    bests_of_gen = []

    # create the initial pool of gen 0
    gen_pool = []
    for _ in range(config.GEN_POOL):
        species = [create(input_output, lane_num=config.LANES, lane_size=config.LANES_SIZE) for _ in range(config.POPULATION)]
        gen_pool.append(species)

    size_penalty = False
    for generations_count in range(config.GENERATIONS):

        pop = config.POPULATION - 5 if generations_count % config.GENERATION_CROSSOVER <= config.GENERATION_CROSSOVER_DURATION < generations_count else config.POPULATION
        gen_pool_t = []
        bests_of_gen = []
        gen_bests = []
        start = time.time()
        for species_index, species in enumerate(gen_pool):

            the_best_of_the_species, y, gen_score_list = Evaluation.evaluator(species, generations_count, input_output, size_penalty)

            #print(f"Generation: {count} Fitness-score: {y}") if count % 10 == 0 else None
            if generations_count % 200 == 0:
                print("________________")
                the_best_of_the_species.visual()
                CircuitRun.circuit_run_truth_table(the_best_of_the_species, input_output, debug=True)
                print("________________")

            top_bests_of_the_species = gen_score_list[:top_p]

            new_gen = []
            new_gen.extend(top_bests_of_the_species)

            pop -= len(top_bests_of_the_species)
            create_new_circuit(top_bests_of_the_species, new_gen, pop)

            bests_of_gen.append((the_best_of_the_species, y))
            gen_bests.append(the_best_of_the_species)
            gen_pool_t.append(new_gen)
        time_taken = time.time() - start

        # crossover between gens, still needs improvements because it's too random right now.
        if generations_count % config.GENERATION_CROSSOVER <= config.GENERATION_CROSSOVER_DURATION < generations_count:
            print("------")
            for i in range(len(gen_pool_t)):
                for _ in range(config.CROSSOVER_IN_GEN):
                    baby_best_gen = crossover([gen_bests[i], gen_bests[random.randint(0, len(gen_pool_t) - 1)]])
                    gen_pool_t[i].append(baby_best_gen)

        if generations_count % 30 == 0 < generations_count:
            replace_worst_species_in_pool(bests_of_gen, gen_pool_t, generations_count, input_output, gen_bests)

        print(f"generation {generations_count} fitness score: {list(map(lambda z: z[1], bests_of_gen))}") if generations_count % 1 == 0 else None

        gen_pool = gen_pool_t

        if generations_count >= config.GENERATIONS * config.PENALTY or time_taken > 0.3:
            size_penalty = True
            print("Size Penalty activated!") if generations_count == config.GENERATIONS * config.PENALTY else None
        else:
            size_penalty = False

    best_score = 0
    for best_g in bests_of_gen:
        if best_g[1] > best_score:
            print(best_g[1])
            best_score = best_g[1]
            the_very_best = best_g[0]

    return the_very_best


def create_new_circuit(bests, new_gen, pop):
    for _ in range(round((pop / 2))):
        mutated_random_best = find_random_best_and_mutate(bests, config.MUTATION_RATE)
        new_gen.append(mutated_random_best)
    for _ in range(round((pop / 2))):
        baby_best = crossover_best(bests)
        baby_best_mutated = mutate(baby_best, config.MUTATION_RATE)
        new_gen.append(baby_best_mutated)


def select_parents():
    return


def replace_worst_species_in_pool(bests_of_gen, gen_pool_t, generations_count, input_output, bests):
    worst_check = 0
    worst_check_select = 0
    for i, worst_for_check in enumerate(bests_of_gen):
        if worst_for_check[1] > worst_check:
            worst_check = worst_for_check[1]
            worst_check_select = i
    gen_pool_t.remove(gen_pool_t[worst_check_select])
    gen_pool_t.append([crossover_best(bests) for _ in
                       range(config.POPULATION)])


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