from circuit import Visualizer


class CircuitObjekt:

    def __init__(self, lanes, gates):
        self._lanes_ = lanes
        self._gates_ = gates
        self._is_new_ = True
        self._score_ = float('inf')
        self._score_with_penalty_ = float('inf')


    def __getitem__(self) -> tuple[list, list]:
        return self._lanes_, self._gates_


    def get_gate_length(self) -> int:
        return len(self._gates_)


    def set_is_circuit_new(self, state: bool):
        self._is_new_ = state


    def is_circuit_new(self) -> bool:
        return self._is_new_


    def set_score(self, new_score: float, new_score_with_penalty: float):
        self._score_ = new_score
        self._score_with_penalty_ = new_score_with_penalty


    def get_score(self) -> tuple[float, float]:
        return self._score_, self._score_with_penalty_


    def visual(self):
        Visualizer.visualizer(self._lanes_, self._gates_)