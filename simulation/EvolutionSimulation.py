import multiprocessing
import random
import time
from functools import partial

import settings
from circuit.CircuitObject import CircuitObjekt
from circuit_management.Create import create
from circuit_management.Crossover import crossover
from circuit_management.Mutate import mutate
from simulation import Evaluation
from simulation.Species import Species

config = settings.EvolutionConfig()


def run_all(truth_table):
    generation_number = 0
    gene_pool = prepare_first_generations(truth_table, generation_number)

    for generation_number in range(config.GENERATIONS):
        gene_pool_eval = run_simulation(gene_pool, truth_table, size_penalty=False)

        print(f"Generation: {generation_number} fitness score: {list(map(lambda z: z.get_best().get_score()[0], gene_pool_eval))}")

        gene_pool = prepare_next_generation(gene_pool_eval, generation_number, size_penalty=False)
        generation_number += 1


def prepare_first_generations(truth_table, generation: int):

    start = time.time()
    gene_pool = []
    for _ in range(config.GEN_POOL):
        species = Species([create(truth_table, lane_num=config.LANES, lane_size=config.LANES_SIZE) for _ in
                                range(config.POPULATION)], generation)
        gene_pool.append(species)
    end = time.time() - start
    print(end)

    return gene_pool


def run_simulation(gene_pool, input_output: list[list], size_penalty: bool):

    worker = partial(Evaluation.evaluator, input_output=input_output)

    # -----Multithreading----- #
    if config.MULTITHREADING:
        with multiprocessing.Pool(processes=config.CORES) as process_pool:
            result = process_pool.map(worker, gene_pool)
    else:
        result = list(map(worker, gene_pool))

    # sort based on size penalty
    penalty = 1 if size_penalty else 0
    for specie in result:
        sorted_specie = sorted(specie.get_circuits(), key=lambda item: item.get_score()[penalty])
        specie.set_circuits(sorted_specie)

    return result


def get_bests(gene_pool, top_amount_to_keep: int):
    if top_amount_to_keep - 1 < 0:
        print("Error, top population too small")
        exit()

    top_best = []
    for best in gene_pool:
        top_circuits = best.get_circuits()[:top_amount_to_keep - 1]

        best.set_circuits(top_circuits)

        top_best.append(best)

    return top_best


def prepare_next_generation(gene_pool_evaluated: list[Species], current_generation: int, size_penalty: bool):
    top: int = round(config.POPULATION * config.TOP_POPULATION)
    new_to_create = config.POPULATION - top

    get_bests(gene_pool_evaluated, top)

    new_species = replace_species(gene_pool_evaluated, current_generation, size_penalty=size_penalty)

    amount_to_mutate = round(new_to_create / 2)

    next_generation = []
    for species_next_generation in gene_pool_evaluated:
        mutated = mutate_circuits(species_next_generation.get_circuits(), amount_to_mutate)
        child_circuit = crossover_circuits(species_next_generation.get_circuits(), new_to_create - amount_to_mutate)
        species_next_generation.set_circuits(mutated + child_circuit)
        next_generation.append(species_next_generation)

    next_generation.extend(new_species)

    return next_generation


def select_parents(certain=None, optional=None, amount_from_optional: int=0) -> list[CircuitObjekt] | None:
    if certain is None:
        certain = []
    if optional is None:
        optional = []
    if len(certain) + len(optional) < 2:
        print(f"Error, not enough parents: {len(certain) + len(optional)}")
        return None
    if amount_from_optional > len(optional):
        print(f"Exception, number too big of optional parents to select of optional parents: {amount_from_optional} > {len(optional)}")
        print("Set to maximum optional parents")
        amount_from_optional = len(optional)

    selected_parents: list = []
    selected_parents.extend(certain)

    for _ in range(amount_from_optional):
        selected_parents.append(optional[random.randint(0, len(optional) - 1)])

    return selected_parents


def mutate_circuits(circuits: list[CircuitObjekt], amount: int) -> list[CircuitObjekt]:

    mutated_circuits = []
    for _ in range(amount):
        mutated = mutate(circuits[random.randint(0, len(circuits) - 1)])
        mutated_circuits.append(mutated)

    return mutated_circuits


def crossover_circuits(circuits: list[CircuitObjekt], amount) -> list[CircuitObjekt]:

    child_circuits = []
    for _ in range(amount):
        parents = select_parents(optional=circuits, amount_from_optional=2)
        child = crossover(parents)
        child_circuits.append(child)

    return child_circuits


def replace_species(circuits: list[Species], current_generation: int, size_penalty: bool):

    penalty = 1 if size_penalty else 0
    number_of_removed = 0
    scores = [s.get_best().get_score()[penalty] for s in circuits]
    top_score = min(scores)
    for i, species in enumerate(circuits):
        if species.get_best().get_score()[penalty] > top_score and species.get_age(current_generation) > 50:
            print(f"Removed: {circuits[i].get_id()} with a score of {circuits[i].get_best().get_score()[penalty]}")
            circuits.remove(circuits[i])
            number_of_removed += 1

    if number_of_removed == 0:
        return []

    return create_new_species(circuits, number_of_removed, current_generation)


def create_new_species(template_circuits: list[Species], amount_of_new_species: int, current_gen: int):

    choice = random.randint(1, 2)
    circuits = []
    x = [circuits + c.get_circuits() for c in template_circuits]

    new_species = []
    new = []
    for _ in range(amount_of_new_species):
        #parent_specie = template_circuits[random.randint(0, len(template_circuits)- 1)].get_circuits()
        if choice == 1:
            new = mutate_circuits(x[0], config.POPULATION)
        if choice == 2:
            new = crossover_circuits(x[0], config.POPULATION)

        new_species.append(Species(new, current_gen))

    return new_species
