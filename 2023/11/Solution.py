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


def main1(k=1):

    # get the field
    field = [list(line) for line in read_input()]

    # check for empty rows
    empty_rows = {idx for idx, row in enumerate(field) if all(ele == "." for ele in row)}
    empty_cols = {cx for cx in range(len(field[0])) if all(row[cx] == "." for row in field)}

    # run from every point at the same time
    queue = collections.deque([(rx, cx, 0, rx*len(field[0])+cx)
                               for rx, row in enumerate(field) for cx, ele in enumerate(row) if ele == '#'])

    visited = {ele[3]: {ele[:2]} for ele in queue}
    shortest_paths = collections.defaultdict(lambda: len(field[0])+len(field)+1)
    while queue:

        # get the current point and make a step
        rx, cx, steps, ident = queue.popleft()

        # make the steps into a direction
        for nrx, ncx, direct in [(rx+1, cx, "v"), (rx-1, cx, "v"), (rx, cx+1, "h"), (rx, cx-1, "h")]:
            if nrx < 0 or ncx < 0 or nrx >= len(field) or ncx >= len(field[0]) or (nrx, ncx) in visited[ident]:
                continue
            if field[nrx][ncx] == "#":
                pair_ident = tuple(sorted((ident, nrx*len(field[0])+ncx)))
                shortest_paths[pair_ident] = min(steps+1, shortest_paths[pair_ident])
                continue
            visited[ident].add((nrx, ncx))
            new_steps = steps + 1
            if direct == "v" and nrx in empty_rows:
                new_steps += k
            elif direct == "h" and ncx in empty_cols:
                new_steps += k
            queue.append((nrx, ncx, new_steps, ident))

    print(f'The result for solution 1 is: {sum(shortest_paths.values())}')


def main2():
    result = 0
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
