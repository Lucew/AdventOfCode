from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect

"""
The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal..
"""


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


# save all the directions if coming from left-above, also save the input directions
#   N
# W X E
#   S
#
DIRECTIONS = {"|": {"N": (1, 0, "N"), "S": (-1, 0, "S")},
              "-": {"W": (0, 1, "W"), "E": (0, -1, "E")},
              "L": {"N": (0, 1, "W"), "E": (-1, 0, "S")},
              "J": {"N": (0, -1, "E"), "W": (-1, 0, "S")},
              "7": {"S": (0, -1, "E"), "W": (1, 0, "N")},
              "F": {"E": (1, 0, "N"), "S": (0, 1, "W")}
              }


def make_update(rx, cx, from_dir, field):

    # get the current symbol we are standing on
    symbol = field[rx][cx]

    # get the new position based on the symbol
    drx, dcx, new_dir = DIRECTIONS[symbol][from_dir]
    rx = rx + drx
    cx = cx + dcx

    # check whether next position is out of bounds or a stone
    if rx < 0 or cx < 0 or rx >= len(field) or cx >= len(field[0]) or field[rx][cx] == ".":
        return -1, -1, None

    # check whether we can not continue as the new symbol does not accept our origin
    if new_dir not in DIRECTIONS[field[rx][cx]]:
        return -1, -1, None

    return rx, cx, new_dir


def path_finding(rx, cx, from_dir, field):

    # construct the current tuple
    curr = (rx, cx, from_dir)

    # make a path variable to save the path positions
    path = set()

    # go into the loop
    steps = 0
    result = 0
    while curr[-1] is not None:

        # make the update to the positions
        curr = make_update(*curr, field)

        # increase the step counter
        steps += 1

        # add to the path
        path.add((curr[0], curr[1]))

        # check whether we reached the end
        if curr[0] == rx and curr[1] == cx:
            result = max(result, steps // 2)
            break
    return result, path


def main1():

    # get the inputs into a matrix
    field = [list(line) for line in read_input()]

    # find the starting positions
    sx = [-1, -1]
    for rx, row in enumerate(field):
        for cx, ele in enumerate(row):
            if ele == "S":
                sx = [rx, cx]

    # check that we found the starting position
    assert sx[0] != -1 and sx[1] != -1, "We did not find the starting position."

    # go through the staring positions possible values and try if it makes a loop and what the farthest
    # point of that loop is
    ps = ""
    result = 0
    path = set()
    for ps, dirs in DIRECTIONS.items():

        # set the symbol to try it
        field[sx[0]][sx[1]] = ps

        # find one of the possible symbol exit incoming directions
        fromdir = list(dirs.keys())[0]

        # find whether we have a valid path
        result, path = path_finding(sx[0], sx[1], fromdir, field)
        if result:
            break

    # check whether we found a solution
    if not result:
        ValueError(f"Something went wrong with the pathfinding.")
    print(f'The result for solution 1 is: {result}')
    return path, field, ps, sx


INFLATIONS = {"|": [['.', '|', '.'], ['.', '|', '.'], ['.', '|', '.']],
              "-": [['.', '.', '.'], ['-', '-', '-'], ['.', '.', '.']],
              "L": [['.', '|', '.'], ['.', 'L', '-'], ['.', '.', '.']],
              "J": [['.', '|', '.'], ['-', 'J', '.'], ['.', '.', '.']],
              "7": [['.', '.', '.'], ['-', '7', '.'], ['.', '|', '.']],
              "F": [['.', '.', '.'], ['.', 'F', '-'], ['.', '|', '.']],
              ".": [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]}


def main2():

    # get the input with the correct set start element
    path, field, ps, sx = main1()

    # construct and inflated field
    inflated_field = []
    for line in field:
        for new_line in range(3):
            inflated_field.append([infl for ele in line for infl in INFLATIONS[ele][new_line]])
    field = inflated_field

    # compute the starting position from the inflated field
    rx = sx[0]*3+1
    cx = sx[1]*3+1

    # make the path finding for the new positions
    fromdir = list(DIRECTIONS[inflated_field[rx][cx]].keys())[0]
    _, path = path_finding(rx, cx, fromdir, inflated_field)

    # make bfs from every position that is not a bath and end if we either meet the outside (not enclosed)
    # or we meet the path
    visited = set()
    result = 0
    for rx, row in enumerate(field):
        for cx, ele in enumerate(row):

            # check whether we visited already or it is element of the path
            if (rx, cx) in visited or (rx, cx) in path:
                continue

            # we can make bfs from here and keep a bfs visiting set to find the result
            bfs_visit = {(rx, cx), }
            queue = [(rx, cx)]
            met_outside = False
            while queue:

                # get the current position
                crx, ccx = queue.pop()

                # go to the surroundings
                for nrx, ncx in [(crx+1, ccx), (crx-1, ccx), (crx, ccx+1), (crx, ccx-1), (crx+1, ccx+1), (crx-1, ccx-1), (crx-1, ccx+1), (crx+1, ccx-1)]:

                    # check whether we have been here or whether it is part of path
                    if (nrx, ncx) in bfs_visit or (nrx, ncx) in path:
                        continue

                    # check whether we are on the outside (so we are not part of the enclosed section)
                    if nrx < 0 or ncx < 0 or nrx >= len(field) or ncx >= len(field[0]):
                        met_outside = True
                        continue

                    # we found a new unvisited field
                    bfs_visit.add((nrx, ncx))
                    queue.append((nrx, ncx))

            # if we never touched the outside we found our result
            if not met_outside:
                result += sum(ele[0] % 3 == 1 and ele[1] % 3 == 1 for ele in bfs_visit)

            # update the visited tiles
            visited.update(bfs_visit)
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main2()
