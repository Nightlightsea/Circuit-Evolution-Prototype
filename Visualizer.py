from LogicGates import list_of_logic_gates


def visualizer(lanes, gates):

    lane_count = 0
    lane = {}
    for x in range(len(lanes)):
        for y in range(len(lanes[x])):
            lane[f"[{x}, {y}]"] = f"{x}.{y}"
            lane_count += 1

    the_gate = "failed to get gate"
    gate_count = 0
    for gate in gates:
        x = str(gate[0]).split(" ")[1]
        for u in list_of_logic_gates:
            if x == str(u[0]).split(" ")[1]:
                the_gate = f"{u[3]}{gate_count}"
                break

        for inputs in gate[1]:
            print(f"{lane[f"{inputs}"]} --> {the_gate}")

        for outputs in gate[2]:
            print(f"{the_gate} --> {lane[f"{outputs}"]}")

        gate_count += 1

