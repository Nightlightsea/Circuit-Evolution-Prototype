import settings
from CircuitRun import circuit_run_truth_table
from EvoSim import build_gen


if __name__ == '__main__':

    truth_table = settings.truth_table_4_in_4_out_logic1

    # run simulation and get the best result
    best_Best = build_gen(truth_table)

    # visualize the best result
    print("_______________________")
    best_Best.visual()
    circuit_run_truth_table(best_Best, truth_table, debug=True)
    print(best_Best.__getitem__()[1])
