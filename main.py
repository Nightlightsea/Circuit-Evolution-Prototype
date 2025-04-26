from time import sleep

import settings
from CircuitRun import circuit_run_truth_table
from EvoSim import run_simulation

config = settings.EvolutionConfig()

if __name__ == '__main__':

    truth_table = settings.decimal_to_binary

    # run simulation and get the best result
    if config.MULTITHREADING:
        print(f"Starting simulation using {config.CORES} cores.Generations: {config.GENERATIONS}, Population: {config.POPULATION}.")
    else:
        print("Starting simulation without multithreading")
    sleep(2)
    the_best = run_simulation(truth_table)

    # visualize the best result
    print("_______________________")
    the_best.visual()
    circuit_run_truth_table(the_best, truth_table, debug=True)
    print(the_best.__getitem__()[1])
