from circuit import Visualizer


class CircuitObjekt:

    def __init__(self, lanes, gates):
        self._lanes_ = lanes
        self._gates_ = gates
        self._score = float('inf')
        self._last_changed = float('inf')

    def __getitem__(self) -> tuple[list,list]:
        return self._lanes_, self._gates_

    def get_gate_length(self):
        return len(self._gates_)

    def set_score(self, new_score: float, change: int):
        self._score = new_score
        self._last_changed = change

    def get_score(self):
        return self._score

    def get_last_change(self):
        return self._last_changed

    def visual(self):
        Visualizer.visualizer(self._lanes_, self._gates_)