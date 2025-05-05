from LogicGates import list_of_logic_gates


def visualizer(lanes, gates):

    node_count = 0
    lane = {}
    for x in range(len(lanes)):
        for y in range(len(lanes[x])):
            if x == 0:
                lane[f"[{x}, {y}]"] = f"{x}.{y}[Input Node {y}]"
            elif x == len(lanes) - 1:
                lane[f"[{x}, {y}]"] = f"{x}.{y}[Output Node {y}]"
            else:
                lane[f"[{x}, {y}]"] = f"{x}.{y}[layer {x} Node {y}]"
            node_count += 1

    the_gate = "failed to get gate"
    gate_count = 0
    for gate in gates:
        x = str(gate[0]).split(" ")[1]
        for u in list_of_logic_gates:
            if x == str(u[0]).split(" ")[1]:
                the_gate = f"{gate_count}[{u[3]} {'-'.join([str(inh) for inh in gate[3]])}]"
                break

        for i, inputs in enumerate(gate[1]):
            if "cable" in the_gate:
                print(f"{lane[f"{inputs}"]} --> ", end="")
            else:
                print(f"{lane[f"{inputs}"]} -- \"in{i}\" --> {the_gate}")

        for o, outputs in enumerate(gate[2]):
            if "cable" in the_gate:
                print(f"{lane[f"{outputs}"]}")
            else:
                print(f"{the_gate} -- \"out{o}\" --> {lane[f"{outputs}"]}")

        gate_count += 1

