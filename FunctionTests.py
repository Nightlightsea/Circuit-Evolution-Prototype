from circuit_management.Mutate import mutate
from circuit_management.Create import create
from circuit_management.Crossover import crossover

if __name__ == '__main__':
    empty_test_truth_table = [[[0,0,0],[0,0,0]]]

    circ_one = create(empty_test_truth_table,3, 3)
    circ_two = create(empty_test_truth_table, 3, 3)

    print("circ 1")
    circ_one.visual()
    print("-----")
    print("circ 2")
    circ_two.visual()
    print("-----")
    print("circ 1 mutated")
    circ_one_mutated = mutate(circ_one, 0.8)
    circ_one_mutated.visual()
    print("-----")
    print("Crossover")
    circ_baby = crossover([circ_one, circ_two])
    circ_baby.visual()