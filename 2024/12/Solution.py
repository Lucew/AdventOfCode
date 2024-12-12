import collections
import itertools
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

    # read the input
    garden = read_input()
    m = len(garden)
    n = len(garden[0])

    # go through the regions and make BFS while keeping track of outside
    # fence number
    visited = set()
    gardens = collections.defaultdict(lambda: [0, 0])
    for __rx, row in enumerate(garden):
        for __cx, plant in enumerate(row):

            # check whether we already visited
            if (__rx, __cx) in visited:
                continue

            # set up a dictionary that keeps track what we visited
            stack = [(__rx, __cx)]
            outside_count = 0
            cur_visited = {(__rx, __cx)}
            while stack:

                # get current position
                rx, cx = stack.pop()

                # go through the neighbors
                for nrx, ncx in [(rx+1, cx), (rx-1, cx), (rx, cx+1), (rx, cx-1)]:

                    # we are not at the outside or in another garden
                    if 0 <= nrx < m and 0 <= ncx < n and garden[nrx][ncx] == plant:
                        # check whether we visited this garden tile before
                        if (nrx, ncx) not in cur_visited:
                            cur_visited.add((nrx, ncx))
                            stack.append((nrx, ncx))
                    else:
                        outside_count += 1

            # update the garden dict
            gardens[__rx, __cx] = [len(cur_visited), outside_count]
            visited.update(cur_visited)
    print(f'The result for solution 1 is: {sum(garden[0]*garden[1] for garden in gardens.values())}')


def main2():

    # read the input
    garden = read_input()
    m = len(garden)
    n = len(garden[0])

    # go through the regions and make BFS while keeping track of outside
    # fence number
    visited = set()
    gardens = collections.defaultdict(lambda: [0, 0])
    for __rx, row in enumerate(garden):
        for __cx, plant in enumerate(row):

            # check whether we already visited
            if (__rx, __cx) in visited:
                continue

            # set up a dictionary that keeps track what we visited
            stack = [(__rx, __cx)]
            cur_visited = {(__rx, __cx)}

            # go through the garden
            outside_plants = {'row': collections.defaultdict(list), 'col': collections.defaultdict(list)}
            while stack:

                # get current position
                rx, cx = stack.pop()

                # go through the neighbors
                for nrx, ncx, typed in [(rx+1, cx, 'row'), (rx-1, cx, 'row'), (rx, cx+1, 'col'), (rx, cx-1, 'col')]:

                    # we are not at the outside or in another garden
                    if 0 <= nrx < m and 0 <= ncx < n and garden[nrx][ncx] == plant:
                        # check whether we visited this garden tile before
                        if (nrx, ncx) not in cur_visited:
                            cur_visited.add((nrx, ncx))
                            stack.append((nrx, ncx))
                    else:

                        # create specifiers for the current fence (we need to make sure that the fence
                        # small gardens have multiple walls
                        nrx = rx + 0.25*(-1 if rx < nrx else 1)
                        ncx = cx + 0.25*(-1 if cx < ncx else 1)

                        # save the fences per row and column
                        outside_plants[typed][nrx if typed == 'row' else ncx].append(ncx if typed == 'row' else nrx)

            # go through both outside cols and rows
            outside_count = 0
            for types in outside_plants.values():
                for elements in types.values():

                    # sort the elements
                    elements = sorted(elements)

                    # go through and check for brakes
                    outside_count += 1
                    for idx, ele in enumerate(elements[1:]):
                        outside_count += abs(elements[idx]-ele) != 1

            # update the garden dict
            gardens[(__rx, __cx)] = [len(cur_visited), outside_count]
            visited.update(cur_visited)
    print(f'The result for solution 2 is: {sum(garden[0] * garden[1] for garden in gardens.values())}')


if __name__ == '__main__':
    main1()
    main2()
