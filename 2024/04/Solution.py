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


def traversal_generator(rx: int, cx: int, word: str, direction_selector: int):

    # define the directions
    dirs = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    # get the next positions
    nrx, ncx = rx, cx
    for offset, ch in enumerate(word):
        yield ch, nrx, ncx
        nrx += dirs[direction_selector][0]
        ncx += dirs[direction_selector][1]


def main1():
    result = 0

    # get the input and traverse it for x and then do bfs from there
    puzzle = read_input()
    m = len(puzzle)
    n = len(puzzle[0])

    # go through the puzzle and search in each direction once we hit an X
    for rx, row in enumerate(puzzle):
        for cx, ch in enumerate(row):
            if ch == 'X':
                # go through all directions
                for direction in range(8):

                    # keep track whether the word is in there (also make sure the indices are valid)
                    result += all((0 <= nrx < m) and (0 <= ncx < n) and (ch == puzzle[nrx][ncx]) for ch, nrx, ncx in traversal_generator(rx, cx, 'XMAS', direction))

    print(f'The result for solution 1 is: {result}')


def is_chross(rx: int, cx: int, grid: list[str]):
    # check whether we found a middle point
    if grid[rx][cx] != 'A':
        return 0

    # check that it is no at the border
    if rx == 0 or rx == len(grid) - 1 or cx == 0 or cx == len(grid) - 1:
        return 0

    # check whether there are M and S (commented out is a more general way)
    diag1 = sorted((grid[rx-1][cx-1], grid[rx+1][cx+1])) == ['M', 'S']
    diag2 = sorted((grid[rx-1][cx+1], grid[rx+1][cx-1])) == ['M', 'S']
    # diag1 = grid[rx-1][cx-1] in 'MS' and grid[rx+1][cx+1] in 'MS' and grid[rx-1][cx-1] != grid[rx+1][cx+1]
    # diag2 = grid[rx-1][cx+1] in 'MS' and grid[rx+1][cx-1] in 'MS' and grid[rx-1][cx+1] != grid[rx+1][cx-1]
    return diag1 and diag2


def main2():
    puzzle = read_input()
    result = sum(is_chross(rx, cx, puzzle) for rx, row in enumerate(puzzle) for cx, ele in enumerate(row))
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
