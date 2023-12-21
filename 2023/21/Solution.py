import collections
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect
import math


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def main1(target_steps=64, lines=None):

    # get the lines if we have not already loaded them
    solution = False
    stop = False
    if lines is None:
        solution = True
        stop = True
        lines = read_input()

    # find the starting position
    start = [-1, -1]
    for rx, row in enumerate(lines):
        for cx, ele in enumerate(row):
            if ele == "S":
                start = [rx, cx]

    # make a queue to do bfs
    stack = collections.deque([(start[0], start[1], 0)])
    visited = {(start[0], start[1]): 0}
    while stack:

        # get the elf position
        rx, cx, steps = stack.popleft()

        # check whether we reached target steps
        if steps == target_steps:
            continue

        # go to the next position
        for nrx, ncx in [(rx+1, cx), (rx-1, cx), (rx, cx+1), (rx, cx-1)]:
            if stop and (nrx < 0 or nrx >= len(lines) or ncx < 0 or ncx >= len(lines[0])):
                continue
            if (nrx, ncx) in visited or lines[nrx % len(lines)][ncx % len(lines[0])] == "#":
                continue
            stack.append((nrx, ncx, steps+1))
            visited[(nrx, ncx)] = steps+1
    assert start[0] != -1 and start[1] != -1, 'Did not find starting position.'

    # go through the visited and check
    result = 0
    for val in visited.values():
        result += (1 - ((target_steps-val) & 1))

    if solution:
        print(f'The result for solution 1 is: {result}')
    return result


def calc_parabola_vertex(x1, y1, x2, y2, x3, y3):

    # compute the parameters a, b, c for polynomial ax^2 + bx + c using three points
    denom = (x1-x2) * (x1-x3) * (x2-x3)
    a = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom
    b = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom
    c = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / denom

    return a, b, c


def main2():

    # get the lines
    lines = read_input()
    target_steps = 26501365

    # find the starting position
    start = [-1, -1]
    for rx, row in enumerate(lines):
        for cx, ele in enumerate(row):
            if ele == "S":
                start = [rx, cx]

    # make some assertions to check whether assumptions hold
    assert len(lines) == len(lines[0]), "Input is not square."
    assert start[0] != -1 and start[1] != -1, "Did not find Start."
    assert all(ele != "#" for ele in lines[start[0]]), "Line is not highway."
    assert all(lines[rx][start[1]] != "#" for rx in range(len(lines))), "Column is not highway."

    # the function is a quadratic, so we find the first three values and can fit the polynomial
    # it is then only approximate, but it works due to the high number and the assumptions above

    # find the index of the first point
    first_point = target_steps % len(lines)

    # make the results for three points
    points = [(x*len(lines)+first_point, main1(x*len(lines)+first_point, lines)) for x in range(3)]

    # fit the polynomial
    a, b, c = calc_parabola_vertex(*(ele for point in points for ele in point))

    print(f'The result for solution 2 is: {math.ceil(a*target_steps**2 + b*target_steps + c)}')


if __name__ == '__main__':
    main1()
    main2()
