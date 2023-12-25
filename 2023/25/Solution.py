import collections
import functools
import itertools
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect
import random


def read_input(path: str = 'input.txt'):
    inputs = collections.defaultdict(set)
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()

            name, connections = line.split(": ")
            connections = connections.split(" ")
            inputs[name].update(connections)
            for connection in connections:
                inputs[connection].add(name)
    return inputs


def kargers_min_cut(graph, t):
    # https://en.wikipedia.org/wiki/Karger%27s_algorithm

    # make a dict to keep track how many components have merged into a combined node
    component_count = {key: 1 for key in graph.keys()}

    while len(graph) > t:
        start = random.choice(list(graph.keys()))
        finish = random.choice(graph[start])

        # Adding the edges from the absorbed node
        for edge in graph[finish]:
            if edge != start:  # this stops us from making a self-loop
                graph[start].append(edge)

        # Deleting the references to the absorbed node and changing them to the source node
        for edge in graph[finish]:
            graph[edge].remove(finish)
            if edge != start:  # this stops us from re-adding all the edges in start
                graph[edge].append(start)

        # keep track of the component counts
        component_count[start] += component_count[finish]
        del component_count[finish]
        del graph[finish]

    # # Calculating and recording the mincut
    conns = graph[list(graph.keys())[0]]
    return conns, component_count


"""
def main1():

    # get the inputs
    graph = read_input()
    nodes = list(graph.keys())

    # get all the edges so we can cut them
    edges = set()
    for val, targets in graph.items():
        edges.update(tuple(sorted((val, ele))) for ele in targets)
    edges = list(edges)

    # make bruteforce solution
    result = -1
    for cutted in itertools.combinations(edges, 3):

        # make a set from the cutted connections
        cutted = set(cutted)

        # make a dfs to find components
        stack = [nodes[0]]
        visited = {nodes[0]}
        while stack:

            # get the current positions
            position = stack.pop()

            # go through the neighbors
            for neighbor in graph[position]:
                if neighbor in visited or (position, neighbor) in cutted or (neighbor, position) in cutted:
                    continue
                stack.append(neighbor)
                visited.add(neighbor)

        # check the size
        if len(visited) < len(nodes):
            result = (len(nodes)-len(visited))*len(visited)
            break

    assert result != -1, "Did not find a solution."
    print(f'The result for solution 1 is: {result}')
"""


def main1():
    # get the inputs
    graph = read_input()

    # go as long as we did not find it
    result = -1
    while True:
        # make a copy of the graph
        ng = dict()
        for val, ele in graph.items():
            ng[val] = list(ele)

        # make the mincut
        conns, component_count = kargers_min_cut(ng, 2)

        # check how many connections are left
        if len(conns) == 3:
            result = functools.reduce(lambda x, y: x*y, component_count.values(), 1)
            break
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
