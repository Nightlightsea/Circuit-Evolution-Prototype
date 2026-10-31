import random

from circuit.CircuitObject import CircuitObjekt


class Species:
    def __init__(self, circuits, birth: int):
        self.specie_id: int = random.randint(0, 99999999)
        self.circuit_list: list[CircuitObjekt] = circuits
        self.birth_generation = birth

    def get_id(self):
        return self.specie_id

    def get_best(self):
        return self.circuit_list[0]

    def get_circuits(self) -> list[CircuitObjekt]:
        return self.circuit_list

    def get_age(self, current_generation: int) -> int:
        return current_generation - self.birth_generation

    def set_circuits(self, new_circuits: list[CircuitObjekt]):
        self.circuit_list = new_circuits
