from typing import Any

from circuit import CircuitObject
import settings
from circuit.CircuitObject import CircuitObjekt
from circuit.RunCircuit import execute_circuit
from simulation.Species import Species

config = settings.EvolutionConfig()


def evaluator(species: Species, input_output) -> Species:

    specie_sort_list = []
    for index, circuit in enumerate(species.get_circuits()):
        if circuit.is_circuit_new(): # if it's a new circuit, compute it's score.
            score_normal, _ = circuit_run_truth_table(circuit, input_output)
            score_penalty = score_normal + circuit.get_gate_length()
            circuit.set_score(score_normal, score_penalty)
            circuit.set_is_circuit_new(False)

        # If the gate penalty is activated, add the number of gates to the score.
        #specie_score: float = circuit.get_score()[1] if size_penalty else circuit.get_score()[0]
        #specie_sort_list = species.get_circuits()


    #specie_score_sorted: list[CircuitObjekt] = sorted(specie_sort_list, key=lambda item: item.get_score()[0])
    #species.set_circuits(specie_score_sorted)
    return species


def circuit_run_truth_table(circuit: CircuitObject.CircuitObjekt, truth_table, debug=False) -> tuple[int | Any, str]:
    initial_lanes, gates = circuit.__getitem__()
    score = 0
    stab = 0
    debug_text = ""

    for truth_table_row in truth_table:

        output_lanes, stab = execute_circuit(gates, initial_lanes, truth_table_row)
        x, db = calculate_score(debug, output_lanes, truth_table_row)
        score += x
        debug_text += f"\n{db}"
        score += stab * (score * 0.1)

    return  score * 100, debug_text

def calculate_score(debug, lanes, truth_table_row):
    scores: float = 0
    factor: float = sum([0 if lanes[-1][x] == truth_table_row[1][x] else 1 for x in range(len(lanes[-1]))])

    debug_result = f"got: {lanes[-1]} expected: {[x for x in truth_table_row[1]]} diff: {factor}"
    #print(f"got: {debug_result}") if debug else None

    for t_t, check in enumerate(lanes[-1]):
        try:
            abs1: float = abs(check - truth_table_row[1][t_t])
        except OverflowError:
            abs1: float = float("inf")
        #abs1 = 1 if abs1 == 0 else abs1
        #abs1 = 100 * (abs1 / abs1 + 10 ) + (factor * 10)
        scores += abs1 * abs1 * factor #* (factor*10)
    return scores, debug_result
