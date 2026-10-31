from time import sleep

from truth_tables import TestTables
import settings
from simulation.Evaluation import circuit_run_truth_table
from simulation.EvoSim import run_simulation
from simulation.EvolutionSimulation import run_all


def main():
    config = settings.EvolutionConfig()
    truth_table = TestTables.truth_table_4_in_4_out_logic1

    # run simulation and get the best result
    if config.MULTITHREADING:
        print(f"Starting simulation using {config.CORES} cores.Generations: {config.GENERATIONS}, Population: {config.POPULATION}.")
    else:
        print("Starting simulation without multithreading")
    sleep(2)

    run_all(truth_table)


    #the_best = run_simulation(truth_table)

    # visualize the best result
    #print("_______________________")
    #the_best.visual()
    #circuit_run_truth_table(the_best, truth_table, debug=True)
    #print(the_best.__getitem__()[1])


if __name__ == '__main__':
    main()
