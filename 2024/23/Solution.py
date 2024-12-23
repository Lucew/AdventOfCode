import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line.split("-"))
    return inputs


def find_components(network_connections: dict[str: set[str]]):
    # find interconnected components of size 3
    # by using bfs and also check that they are connected with each other
    # (each of them has two connections)
    visited = set()
    largest_size = 0
    largest_component = set()
    for st in network_connections.keys():

        # check whether we have been here
        if st in visited:
            continue

        # use a dfs and visited tracker for traversing all nodes
        curr_visited = {st}
        stack = [st]
        connections_number = set()
        while stack:

            # get the current position
            curr = stack.pop()

            # add the number of connections to the set
            connections_number.add(len(network_connections[curr]))

            # go through the neighbors
            for neigh in network_connections[curr]:
                if neigh not in curr_visited:
                    stack.append(neigh)
                    curr_visited.add(neigh)

        # check whether it is fully connected and how large it is
        node_number = len(curr_visited)
        if (len(connections_number) == 1 and node_number in connections_number) and node_number > largest_size:
            largest_size = node_number
            largest_component = curr_visited

        # add to the visited
        visited.update(curr_visited)
    return largest_component


def main1():
    result = 0

    # get the network
    network = read_input()

    # build a graph from the network
    network_connections = collections.defaultdict(set)
    for st, ta in network:
        network_connections[st].add(ta)
        network_connections[ta].add(st)

    # find sets of three, where the intersection is longer than two
    components = set()
    for st, st_connt in network_connections.items():
        for ta in st_connt:
            intersect = st_connt.intersection(network_connections[ta])
            components.update({tuple(sorted((st, ta, ele))) for ele in intersect})

    # check for historian components
    for conn in components:
        if any(ele[0] == 't' for ele in conn):
            result += 1
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # get the network
    network = read_input()

    # build a graph from the network
    network_connections = collections.defaultdict(set)
    for st, ta in network:
        network_connections[st].add(ta)
        network_connections[ta].add(st)

    # implement the bron kerbosch algorithm
    # https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm (algorithm version 1)
    result = set()
    def bron_kerbosch(set_r: set[str], set_p: set[str], set_x: set[str]):
        nonlocal result
        if len(set_r) + len(set_p) <= len(result):
            return
        if len(set_p) == 0 and len(set_x) == 0:
            result = result if len(result) > len(set_r) else {ele for ele in set_r}

        # get the current keys
        keys = {ele for ele in set_p}
        for vert in keys:
            bron_kerbosch(set_r | {vert}, set_p & network_connections[vert], set_x & network_connections[vert])
            set_p.remove(vert)
            set_x.add(vert)

    # do binary search over the graph size
    bron_kerbosch(set(), set(network_connections.keys()), set())
    print(f'The result for solution 2 is: {",".join(sorted(result))}')


if __name__ == '__main__':
    main1()
    main2()
