import collections
import heapq
import functools
import bisect
import graphviz


def read_input(path: str = 'input.txt'):
    gates = dict()
    connections = []
    is_connections = False
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()

            if not line:
                is_connections = True
                continue

            if is_connections:
                connections.append(line.split(' '))
            else:
                gate, val = line.split(': ', 1)
                gates[gate] = val == "1"
    return gates, connections


def main1():
    result = 0

    # get the input
    gates, connections = read_input()

    # define the operations
    operations = {'OR': lambda x, y: x | y, 'AND': lambda x, y: x & y, 'XOR': lambda x, y: x ^ y}

    # go through the connections and check whether we have values for them until we are finished
    while connections:
        new_connections = []
        for inp1, operation, inp2, arrow, out in connections:
            if inp1 in gates and inp2 in gates:
                gates[out] = operations[operation](gates[inp1], gates[inp2])
            else:
                new_connections.append((inp1, operation, inp2, arrow, out))
        connections = new_connections

    zs = [0]*64
    for gt, val in sorted((ele for ele in gates.items() if ele[0][0] == 'z')):
        zs[int(gt[1:])] = int(val)
        result += val * (1 << int(gt[1:]))
    while zs[-1] == 0:
        zs.pop()
    print("".join(str(ele) for ele in reversed(zs)))
    print(f'The result for solution 1 is: {result}')


def main2():
    """
    Idea here is: check the output image for switched connections (takes time but works)
    :return:
    """
    result = 0

    # Create a new directed graph
    dot = graphviz.Digraph(format='png', engine='dot')

    # get the input
    gates, connections = read_input()

    # get all nodes (inputs, outputs)
    inps = set(gates.keys())
    for inp1, operation, inp2, arrow, out in connections:
        inps.add(inp1)
        inps.add(inp2)

    # Add operand nodes (inputs/outputs) as circles
    for var in inps:
        dot.node(var, var, shape='circle')  # Circle shape for operands

    # Add operations as nodes (operators in boxes)
    for op in connections:
        input1, gate, input2, _, output = op

        # Create gate node in a box
        gate_label = f'{gate}'
        gate_name = f'{input1}_{input2}_{gate}'  # Unique gate name
        dot.node(gate_name, gate_label, shape='box')  # Box shape for operators

        # Connect inputs to gate
        dot.edge(input1, gate_name)
        dot.edge(input2, gate_name)

        # Connect gate to output
        dot.node(output, output, shape='circle')  # Output node as circle
        dot.edge(gate_name, output)

    # Render the graph to a file
    output_path = 'circuit_graph_sample'
    dot.render(output_path)  # Saves the output to 'circuit_graph.png'

    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
