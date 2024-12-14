from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def main1():

    # get the input into the function
    mapped = read_input()
    m = len(mapped)
    n = len(mapped[0])

    # go through the map and get the position of equal antennas
    antennas = defaultdict(list)
    for rx, row in enumerate(mapped):
        for cx, ele in enumerate(row):
            if ele != '.':
                antennas[ele].append((rx, cx))

    # go through the antennas and create the antinodes
    antinodes = set()
    for positions in antennas.values():
        for idx, pos1 in enumerate(positions):
            for pos2 in positions[idx+1:]:

                # compute the antinode position
                dcx = pos2[1] - pos1[1]
                drx = pos2[0] - pos1[0]
                antinode = [[pos1[0]-drx, pos1[1]-dcx], [pos2[0]+drx, pos2[1]+dcx]]

                # check whether the nodes are in bounds and add to set
                antinodes.update((rx, cx) for rx, cx in antinode if 0 <= rx < m and 0 <= cx < n)
    print(f'The result for solution 1 is: {len(antinodes)}')


def main2():
    # get the input into the function
    mapped = read_input()
    m = len(mapped)
    n = len(mapped[0])

    # go through the map and get the position of equal antennas
    antennas = defaultdict(list)
    for rx, row in enumerate(mapped):
        for cx, ele in enumerate(row):
            if ele != '.':
                antennas[ele].append((rx, cx))

    # go through the antennas and create the antinodes
    antinodes = set()
    for positions in antennas.values():
        for idx, pos1 in enumerate(positions):
            for pos2 in positions[idx + 1:]:

                # compute the antinode distance
                dcx = pos2[1] - pos1[1]
                drx = pos2[0] - pos1[0]

                # start from pos2 and go in both direction until out of bounds
                nrx = pos2[0]
                ncx = pos2[1]
                while 0 <= nrx < m and 0 <= ncx < n:
                    antinodes.add((nrx, ncx))
                    nrx -= drx
                    ncx -= dcx
                nrx = pos2[0]
                ncx = pos2[1]
                while 0 <= nrx < m and 0 <= ncx < n:
                    antinodes.add((nrx, ncx))
                    nrx += drx
                    ncx += dcx
    print(f'The result for solution 2 is: {len(antinodes)}')


if __name__ == '__main__':
    main1()
    main2()
