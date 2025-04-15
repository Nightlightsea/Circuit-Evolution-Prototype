import Visualizer


class CircuitObjekt:

    def __init__(self, lanes, gates):
        self._lanes_ = lanes
        self._gates_ = gates

    def __getitem__(self) -> tuple[list,list]:
        return self._lanes_, self._gates_

    def get_gate_length(self):
        return len(self._gates_)

    def visual(self):
        Visualizer.visualizer(self._lanes_, self._gates_)