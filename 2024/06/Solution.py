import collections
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


def direction_iterator(start: str):

    # set the starting index
    dirs = {'^': 0, '>': 1, 'v': 2, '<': 3}
    sdx = dirs[start]

    # go through the directions
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    while True:
        curr_dir = directions[sdx]
        sdx = (sdx + 1) % len(directions)
        yield curr_dir


def main1(modified_mapped: list[str] = None):

    if modified_mapped is None:
        # get the input
        mapped = read_input()
        mapped = [list(stringi) for stringi in mapped]
    else:
        mapped = modified_mapped
    m = len(mapped)
    n = len(mapped[0])

    # go through every element and save obstructions (sparse matrix) in sorted order
    # per row and column
    rows = collections.defaultdict(list)
    cols = collections.defaultdict(list)
    init_dir = ''
    posi = [0, 0]
    for rx, row in enumerate(mapped):
        for cx, ch in enumerate(row):
            if ch == '#':
                rows[rx].append(cx)
                cols[cx].append(rx)
            elif ch != '.' and ch != '#':
                init_dir = ch
                posi = [rx, cx]
    initial_posi = posi

    # make an iterator of directions
    dirit = direction_iterator(init_dir)
    curdir = next(dirit)

    # go until we are out of bounds
    visited = {(posi[0], posi[1]): curdir}
    while True:

        # compute the update
        nrx = posi[0] + curdir[0]
        ncx = posi[1] + curdir[1]

        # check whether we go out of bounds
        if nrx < 0 or nrx >= m or ncx < 0 or ncx >= n:
            break

        # check whether we would reach and obstacle
        if mapped[nrx][ncx] == '#':
            # update the direction
            curdir = next(dirit)
        else:  # we make another step

            # check whether we are stuck in a loop
            if (nrx, ncx) in visited and visited[(nrx, ncx)] == curdir:
                return True, visited, mapped, initial_posi
            visited[(nrx, ncx)] =  curdir
            posi = [nrx, ncx]

    if modified_mapped is None:
        print(f'The result for solution 1 is: {len(visited)}')
    return False, visited, mapped, initial_posi


def main2():
    result = 0
    # get the initial path of the guard and the input
    _, visited, mapped, initial_posi = main1()

    # go through the path and try to place blocks
    for nrx, ncx in visited:

        # do not place at starting position
        if [nrx, ncx] == initial_posi:
            continue

        # place the obstruction
        mapped[nrx][ncx] = '#'

        # check whether we get into a loop
        looped, _, _, _ = main1(mapped)
        if looped:
            result += 1

        # get rid of the obstruction
        mapped[nrx][ncx] = '.'
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
