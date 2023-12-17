import functools
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append([int(ele) for ele in line])
    return inputs


UPDATES = {"d": (1, 0), "u": (-1, 0), "r": (0, 1), "l": (0, -1)}
DIRLINKS = {"d": "u", "u": "d", "r": "l", "l": "r"}


def main1():

    # get the grid
    grid = read_input()

    # make a dict to save the paths we have already taken
    visited = defaultdict(dict)
    for direction in UPDATES.keys():
        visited[(0, 0)][(direction, 1)] = 0

    # make a heap that saves the paths according to their heat loss
    heap = [(0, "d", 0, 0, 0)]
    result = float("inf")
    while heap:

        # get the current information
        heat, direction, direction_steps, rx, cx = heappop(heap)

        # check whether we found the end
        if rx == len(grid)-1 and cx == len(grid[0])-1:
            result = heat
            break

        # go through all directions
        for ndirection, (drx, dcx) in UPDATES.items():

            # check whether we turned
            if DIRLINKS[ndirection] == direction:
                continue

            # update the coordinates and direction steps
            nrx = rx+drx
            ncx = cx+dcx
            ndir_steps = 1 if ndirection != direction else direction_steps + 1

            # check whether we went out of bounds or made to many steps in one direction
            if nrx < 0 or ncx < 0 or nrx >= len(grid) or ncx >= len(grid[0]) or ndir_steps > 3:
                continue

            # check whether we already have been there (with less steps or equal in that direction)
            if (ndirection, ndir_steps) in visited[(nrx, ncx)]:
                continue

            # we can go there and save our value
            nheat = heat + grid[nrx][ncx]
            visited[(nrx, ncx)][(ndirection, ndir_steps)] = nheat
            heappush(heap, (nheat, ndirection, ndir_steps, nrx, ncx))

    print(f'The result for solution 1 is: {result}')


def main2():

    # get the grid
    grid = read_input()

    # make a dict to save the paths we have already taken
    visited = defaultdict(dict)
    for direction in UPDATES.keys():
        visited[(0, 0)][(direction, 1)] = 0

    # make a heap that saves the paths according to their heat loss
    heap = [(0, "d", 0, 0, 0)]
    result = float("inf")
    while heap:

        # get the current information
        heat, direction, direction_steps, rx, cx = heappop(heap)

        # check whether we found the end
        if rx == len(grid) - 1 and cx == len(grid[0]) - 1:
            result = heat
            break

        # go through all directions
        for ndirection, (drx, dcx) in UPDATES.items():

            # check whether we turned
            if DIRLINKS[ndirection] == direction:
                continue

            # update the coordinates and direction steps (for all the min steps to max steps while keeping track of the
            # heat loss we accumulate
            nheat = heat
            for steps_mult in range(1, 11):

                # update the position
                nrx = rx + drx*steps_mult
                ncx = cx + dcx*steps_mult
                ndir_steps = steps_mult if ndirection != direction else direction_steps + steps_mult

                # check whether we went out of bounds or made to many steps in one direction
                if nrx < 0 or ncx < 0 or nrx >= len(grid) or ncx >= len(grid[0]) or ndir_steps > 10:
                    break

                # check whether we already have been there (then we encountered less heat loss)
                if (ndirection, ndir_steps) in visited[(nrx, ncx)]:
                    break

                # we can go there and save our value
                nheat = nheat + grid[nrx][ncx]

                # check that we make a minimum of four steps
                if steps_mult < 4:
                    continue
                visited[(nrx, ncx)][(ndirection, ndir_steps)] = nheat
                heappush(heap, (nheat, ndirection, ndir_steps, nrx, ncx))

    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
