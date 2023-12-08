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


def find_loop_size(start_node: str, graph: dict[dict[str:str]], instructions_text: str):

    # keep track of the loop
    visited = collections.defaultdict(dict)
    current = start_node
    steps = 0
    instructions = endless_generator(instructions_text)
    next_move, idx = next(instructions)
    while idx not in visited[current]:
        visited[current][idx] = steps
        current = graph[current][next_move]
        next_move, idx = next(instructions)
        steps += 1

    # save the node where the loop starts
    loop_start = current
    loop_length = steps-visited[current][idx]
    until_loop = steps-loop_length

    # go until the loop start and find all targets until then
    targets_till_loop = set()
    current = start_node
    instructions = endless_generator(instructions_text)
    next_move, _ = next(instructions)
    for step in range(until_loop):
        if current.endswith("Z"):
            targets_till_loop.add(step)
        current = graph[current][next_move]
        next_move, _ = next(instructions)

    # targets in loop
    targets_in_loop = set()
    assert current == loop_start, "Something with cycle detection is off."
    for step in range(loop_length):
        if current.endswith("Z"):
            targets_in_loop.add(step)
        current = graph[current][next_move]
        next_move, _ = next(instructions)

    # check for loop in loop
    if len(targets_till_loop) > 1:
        targets = sorted(targets_till_loop)
        targets = [ele - targets[idx - 1] for idx, ele in enumerate(targets)]
        print(targets)

    return targets_till_loop, targets_in_loop, loop_length, until_loop


def ext_gcd(A, B):
    x2, y2, x1, y1, x, y, r2, r1, q, r = 1, 0, 0, 1, 0, 0, A, B, 0, 0

    while r1 != 0:
        q = r2 // r1
        r = r2 % r1
        x = x2 - (q * x1)
        y = y2 - (q * y1)

        x2, y2, x1, y1, r2, r1 = x1, y1, x, y, r1, r

    return x2, y2, r2


def chinese_remainder_theorem(A, M):
    if len(A) != len(M):
        return -1, -1  # Invalid input

    n = len(A)

    a1, m1 = A[0], M[0]

    for i in range(1, n):
        a2, m2 = A[i], M[i]

        g = math.gcd(m1, m2)
        if a1 % g != a2 % g:
            return -1, -1  # No solution exists

        p, q, _ = ext_gcd(m1 // g, m2 // g)

        mod = m1 // g * m2  # LCM of m1 and m2

        x = (a1 * (m2 // g) * q + a2 * (m1 // g) * p) % mod

        a1 = x
        if a1 < 0:
            a1 += mod  # Result is not supposed to be negative
        m1 = mod

    return a1, m1


def main2(bruteforce=True):

    # get the input
    lines = read_input()

    # go through the other lines and build a graph
    graph = collections.defaultdict(dict)
    for line in lines[2:]:
        current, targets = line.split(" = ")
        targets = targets.split(", ")
        graph[current]["L"] = targets[0][1:]
        graph[current]["R"] = targets[1][:-1]

    # start simultaneously at all nodes ending with "A"
    current = [ele for ele in graph.keys() if ele.endswith("A")]

    # get the information about each start position and their circles
    current_info = dict()
    max_circ = 0
    for ele in current:
        current_info[ele] = list(find_loop_size(ele, graph, lines[0]))
        max_circ = max(max_circ, current_info[ele][-1])

    # check whether we have a common solution until then
    before_loop = functools.reduce(lambda x, y: x & y, (ele[0] for ele in current_info.values()))
    if before_loop:
        print(f'The result for solution 2 is: {min(before_loop)}')

    # go to the beginning of the last loop and make corrections to the periods of all the other loops
    for key, (_, ele_in_loop, loop_length, until_loop) in current_info.items():

        # get how many steps we are into the loop
        steps_in = (max_circ-until_loop) % loop_length
        print(steps_in)

        # adapt the periods of the loops as we are somewhere in there
        current_info[key][1] = set((ele-steps_in) % loop_length for ele in ele_in_loop)
        print(current_info[key][1])
    print("sdfsdf2")
    # make all the possible combinations and use chinese modulo rule to solve it
    result = float("inf")
    tuple_generator = set(itertools.product(*[[(e, ele[2]) for e in ele[1]] for ele in current_info.values()]))
    for tupled in tuple_generator:
        print(functools.reduce(lambda x,y: x*y, [ele[1] for ele in tupled]), tupled)
        print(chinese_remainder_theorem(tupled[0], tupled[1]))
        result = min(result, chinese_remainder_theorem(tupled[0], tupled[1])[0])

    print(f'The result for solution 2 is: {result}')


def main22():

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
