import collections
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


# create a directions change for each tile
TILES = {".": {"N": "N", "W": "W", "S": "S", "E": "E"},
         "/": {"N": "E", "W": "S", "S": "W", "E": "N"},
         "\\": {"N": "W", "W": "N", "S": "E", "E": "S"},
         "-": {"N": "EW", "W": "W", "S": "EW", "E": "E"},
         "|": {"N": "N", "W": "NS", "S": "S", "E": "NS"},
         }

# make a dict to lookup updates
UPDATES = {"N": (1, 0), "W": (0, 1), "S": (-1, 0), "E": (0, -1)}


def main1(rx: int = 0, cx: int = 0, direction: str = "W", grid: list[list[str]] = None):

    # get the input into a grid
    grid_given = True
    if grid is None:
        grid = [list(line) for line in read_input()]
        grid_given = False
    m = len(grid)
    n = len(grid[0])

    # make a stack for bfs
    stack = [(rx, cx, direction)]
    visited = collections.defaultdict(set)
    visited[(rx, cx)].add(direction)
    while stack:

        # get the current position and origin (orientation)
        rx, cx, origin = stack.pop()

        # check the new origin (direction change)
        new_origins = TILES[grid[rx][cx]][origin]

        # go through the new directions
        for new_origin in new_origins:

            # get the updated value
            drx, dcx = UPDATES[new_origin]
            nrx = rx+drx
            ncx = cx+dcx

            # check whether we went out of scope
            if nrx < 0 or ncx < 0 or nrx >= m or ncx >= n:
                continue

            # check whether we have been there with same orientation (termination)
            been_there = new_origin in visited[(nrx, ncx)]
            if been_there:
                continue
            else:
                visited[(nrx, ncx)].add(new_origin)

            # put into the stack
            stack.append((nrx, ncx, new_origin))

    if not grid_given:
        print(f'The result for solution 1 is: {len(visited)}')
    return len(visited)


def main2():
    grid = [list(line) for line in read_input()]
    result = 0
    for rx in range(len(grid)):
        tmp = max(main1(rx, 0, "W", grid), main1(rx, len(grid[0])-1, "E", grid))
        result = max(tmp, result)
    for cx in range(len(grid)):
        tmp = max(main1(0, cx, "N", grid), main1(len(grid)-1, cx, "S", grid))
        result = max(tmp, result)
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
