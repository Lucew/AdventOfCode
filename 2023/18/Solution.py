from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            line = line.split(" ")
            line[1] = int(line[1])
            inputs.append(line)
    return inputs


DIRECTIONS = {"U": (-1, 0), "D": (1, 0), "R": (0, 1), "L": (0, -1)}


def main1():

    # get some variables that save the dimension of the field
    start_rx = 0
    end_rx = 0
    start_cx = 0
    end_cx = 0

    # set the starting position and a set which keeps track of the visited positions
    rx, cx = 0, 0
    visited = set()
    visited.add((0, 0))

    for direction, steps, color in read_input():

        # get the step difference
        drx, dcx = DIRECTIONS[direction]

        # make the update
        for _ in range(steps):
            rx += drx
            cx += dcx
            visited.add((rx, cx))

        # update the field size
        start_rx = min(start_rx, rx)
        end_rx = max(end_rx, rx)
        start_cx = min(start_cx, cx)
        end_cx = max(end_cx, cx)

    # now make floodfill on the defined field and the visited digs
    flooded = set()
    result = len(visited)
    for rx in range(start_rx, end_rx+1):
        for cx in range(start_cx, end_cx+1):

            # check whether we flooded it
            if (rx, cx) in flooded or (rx, cx) in visited:
                continue

            # make stack dfs until we go out of bounds or hit the path
            stack = [(rx, cx)]
            curr_flooded = set()
            curr_flooded.add((rx, cx))
            out_of_bounds = False
            while stack:

                # get the positions
                rx, cx = stack.pop()

                # go to the neighbors
                for nrx, ncx in [(rx+1, cx), (rx-1, cx), (rx, cx+1), (rx, cx-1), (rx+1, cx+1), (rx-1, cx-1), (rx+1, cx-1), (rx-1, cx+1)]:

                    # check whether we are out of bounds
                    if nrx < start_rx or ncx < start_cx or nrx > end_rx or ncx > end_cx:
                        out_of_bounds = True
                        continue

                    # check whether we hit a path
                    if (nrx, ncx) in visited:
                        continue

                    # check whether we already visited in this dfs
                    if (nrx, ncx) in curr_flooded:
                        continue

                    # mark it as visited in this dfs
                    curr_flooded.add((nrx, ncx))

                    # append it to the stack
                    stack.append((nrx, ncx))

            # check if this flood was and inner piece
            if not out_of_bounds:
                result += len(curr_flooded)

            # update the flooded fields
            flooded.update(curr_flooded)

    print(f'The result for solution 1 is: {result}')


def main2():

    # get some variables that save the dimension of the field
    start_rx = 0
    end_rx = 0
    start_cx = 0
    end_cx = 0

    # set the starting position and a set which keeps track of the visited positions
    rx, cx = 0, 0
    visited = [(rx, cx)]
    path = 0

    # make a translator for the hexcode
    hex2dir = {"0": "R", "1": "D", "2": "L", "3": "U"}
    result = 0
    for _, _, color in read_input():

        # parse the color code into the digits
        direction = hex2dir[color[-2]]
        steps = int(color[2:-2], 16)

        # get the step difference
        drx, dcx = DIRECTIONS[direction]

        # make the update
        rx += drx*steps
        cx += dcx*steps
        path += steps

        # update the Trapezoid formula from https://en.wikipedia.org/wiki/Shoelace_formula
        result += ((cx+visited[-1][1])*(rx-visited[-1][0]))

        # append the update to the tiles
        visited.append((rx, cx))
    print(f'The result for solution 1 is: {result/2+path/2+1}')


if __name__ == '__main__':
    main1()
    main2()
