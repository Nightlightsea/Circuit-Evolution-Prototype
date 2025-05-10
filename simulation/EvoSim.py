import math
import multiprocessing
import random
import time
from functools import partial
import matplotlib.pyplot as plt

from circuit import CircuitObject
from simulation import Evaluation
import settings
from circuit_management.Mutate import mutate
from circuit_management.Create import create
from circuit_management.Crossover import crossover

config = settings.EvolutionConfig()


def animate_generation(bests_history, ax, fig):

    plt.cla()
    for specie in bests_history:
        gens = []
        score = []
        for generation in bests_history[specie]:
            gens += [generation]
            score += [bests_history[specie][generation]]
        ax.plot(gens, score)

    plt.ylabel('fitness')
    plt.xlabel('generation')

    fig.canvas.draw()
    fig.canvas.flush_events()



def run_simulation(input_output: list) -> CircuitObject.CircuitObjekt:

    top_p = int(config.TOP_POPULATION * config.POPULATION)
    species_id = 0
    best_history = {}

    #plt.ion()
    #fig = plt.figure(figsize=(12, 6))
    #ax = fig.add_subplot(111)

    bests_of_generation_with_score = []

    # create the initial pool of gen 0
    gene_pool = []
    for _ in range(config.GEN_POOL):
        species = [species_id,[create(input_output, lane_num=config.LANES, lane_size=config.LANES_SIZE) for _ in range(config.POPULATION)]]
        species_id += 1
        gene_pool.append(species)

    start: float = time.time() # start timer.
    size_penalty: bool = False
    for current_generation in range(config.GENERATIONS):

        gene_pool_next: list[list] = []
        bests_of_generation_with_score = []

        # -----Multithreading----- #
        worker = partial(Evaluation.evaluator, gen_num=current_generation, input_output=input_output, size_penalty=size_penalty)
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
                Evaluation.circuit_run_truth_table(the_best_of_the_species, input_output, debug=True)
                print("________________")

            #if f'{species_score_list[0]}' not in best_history:
            #    best_history[f'{species_score_list[0]}'] = {}
            #best_history[f'{species_score_list[0]}'][f'{current_generation}'] = score_of_circuit

            #----Prepare the next generation.----#
            top_bests_of_the_species = species_score_list[1][:top_p].copy()
            next_generation_of_species = [species_score_list[0], []]
            next_generation_of_species[1].extend(top_bests_of_the_species)

            population_size -= len(top_bests_of_the_species)
            create_new_circuits(top_bests_of_the_species, next_generation_of_species[1], population_size)

            bests_of_generation_with_score.append((the_best_of_the_species, score_of_circuit, species_score_list[0]))
            gene_pool_next.append(next_generation_of_species)
            # ------------------------------ #

        time_taken: float = time.time() - start

        #if current_generation % 10 == 0:
        #    animate_generation(best_history, ax, fig)

        # crossover between species.
        if current_generation % config.GENERATION_CROSSOVER <= config.GENERATION_CROSSOVER_DURATION < current_generation:
            print("------")
            for i in range(len(gene_pool_next)):
                for _ in range(config.CROSSOVER_IN_GEN):
                    baby_best_gen = crossover([bests_of_generation_with_score[i][0], bests_of_generation_with_score[random.randint(0, len(gene_pool_next) - 1)][0]])
                    gene_pool_next[i][1].append(baby_best_gen)

        # removing a species if they are worse than the best by a factor.
        if current_generation % 20 == 0 < current_generation:
           species_id = replace_worst_species_in_pool(bests_of_generation_with_score, gene_pool_next, current_generation, input_output, species_id)

        time_estimate = (time_taken / (current_generation + 1)) * (config.GENERATIONS - current_generation)
        minutes = time_estimate / 60
        seconds = time_estimate % 60
        print(f"generation: {current_generation} time estimate: {math.floor(minutes)}:{round(seconds)} fitness score: {list(map(lambda z: z[1], bests_of_generation_with_score))}") if current_generation % 1 == 0 else None

        gene_pool = gene_pool_next

        if current_generation >= config.GENERATIONS * config.PENALTY: # or current_generation % 400 > 390:
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


def replace_worst_species_in_pool(bests_of_gen, gen_pool_t, generations_count, input_output, specie_id):
    num_species = len(bests_of_gen)
    if num_species < 2:
        # Need at least two species to compare and potentially remove one
        return None

    scores              = [circ[1] for circ in bests_of_gen]
    bests               = [best_c[0] for best_c in bests_of_gen]
    best_score          = min(scores)
    worst_check_select  = -1
    worst: float        = 0
    max_removal         = 2
    removed             = 0
    for i, worst_for_check in enumerate(bests_of_gen):
        if worst <= worst_for_check[1] > best_score * 1.1 and i < len(bests_of_gen) * 0.7 and removed <= 3:
            worst_check_select = worst_for_check[2]
            worst = worst_for_check[1]
            removed += 1

            for gene_index in range(len(gen_pool_t) - 1):
                if gen_pool_t[gene_index][0] == worst_for_check[2]:

                    print(f"Removing species: {worst_check_select} with a score of {bests_of_gen[i][1]}")
                    specie_id += 1
                    new_species = [specie_id, []]
                    at_random_crossover_mutation_creation = random.randint(1, 3)

                    if at_random_crossover_mutation_creation == 1:
                        new_species[1].extend([crossover_best(bests) for _ in
                                       range(config.POPULATION)])

                    if at_random_crossover_mutation_creation == 2:
                        create_new_circuits(bests, new_species[1], config.POPULATION)

                    if at_random_crossover_mutation_creation == 3:
                        new_species[1].extend([create(input_output, lane_num=config.LANES, lane_size=config.LANES_SIZE) for _ in
                                            range(round(config.POPULATION))])

                    gen_pool_t.remove(gen_pool_t[gene_index])
                    gen_pool_t.append(new_species)
    return specie_id



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