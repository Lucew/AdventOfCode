import collections
import functools
import math
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect
import itertools


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def endless_generator(instructions: str):
    idx = 0
    while True:
        yield instructions[idx]
        idx = (idx + 1) % len(instructions)


def main1():
    result = 0

    # get the input
    lines = read_input()
    instructions = endless_generator(lines[0])

    # go through the other lines and build a graph
    graph = collections.defaultdict(dict)
    for line in lines[2:]:
        current, targets = line.split(" = ")
        targets = targets.split(", ")
        graph[current]["L"] = targets[0][1:]
        graph[current]["R"] = targets[1][:-1]

    # go through the graph until we find "ZZZ"
    current = "AAA"
    for next_move in instructions:
        current = graph[current][next_move]
        result += 1
        if current == "ZZZ": break
    print(f'The result for solution 1 is: {result}')


def main2():

    # get the input
    lines = read_input()

    # go through the other lines and build a graph
    graph = collections.defaultdict(dict)
    for line in lines[2:]:
        current, targets = line.split(" = ")
        targets = targets.split(", ")
        graph[current]["L"] = targets[0][1:]
        graph[current]["R"] = targets[1][:-1]

    # find all nodes ending with "A"
    starts = [ele for ele in graph.keys() if ele.endswith("A")]
    path_length = {ele: 0 for ele in starts}
    for start in starts:

        # get the path length
        current = start
        steps = 0
        instructions = endless_generator(lines[0])
        while not current.endswith("Z"):
            steps += 1
            next_move = next(instructions)
            current = graph[current][next_move]
        path_length[start] = steps

    # compute the result by using gcd
    result = functools.reduce(math.lcm, path_length.values())
    print(path_length)
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
