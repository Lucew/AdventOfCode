import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def check_neighbours(rx, cx, field):
    sourroundercounter = 0
    for nrx, ncx in ((rx+1, cx),(rx-1, cx),(rx, cx+1),(rx, cx-1),(rx+1, cx+1),(rx+1, cx-1),(rx-1, cx+1),(rx-1, cx-1)):
        if 0 <= nrx < len(field) and 0 <= ncx < len(field[0]):
            sourroundercounter += field[nrx][ncx] == '@'
    return sourroundercounter



def main1():
    result = 0

    # go through the field and check how many neighbours they have
    field = read_input()
    for rx, row in enumerate(field):
        for cx, ele in enumerate(row):
            if field[rx][cx] == '@':
                result += check_neighbours(rx, cx, field) < 4
    print(f'The result for solution 1 is: {result}')


def update_neighbours(rx, cx, counter):
    new_neighbours = []
    for nrx, ncx in ((rx+1, cx),(rx-1, cx),(rx, cx+1),(rx, cx-1),(rx+1, cx+1),(rx+1, cx-1),(rx-1, cx+1),(rx-1, cx-1)):
        if (nrx, ncx) in counter:
            if counter[(nrx, ncx)] == 4:
                new_neighbours.append((nrx, ncx))
            counter[(nrx, ncx)] -= 1
    return new_neighbours


def main2():
    result = 0

    # go through the field and check how many neighbours they have
    field = read_input()
    counter = collections.Counter()
    stack = []
    for rx, row in enumerate(field):
        for cx, ele in enumerate(row):
            if field[rx][cx] == '@':
                counter[rx, cx] = check_neighbours(rx, cx, field)
                if counter[rx, cx] < 4:
                    stack.append((rx, cx))
                    result += 1

    # now do a dfs on the roll positions
    while stack:

        # go through the current positions
        new_stack = []
        for rx, cx in stack:
            new_neighbours = update_neighbours(rx, cx, counter)
            new_stack.extend(new_neighbours)
            result += len(new_neighbours)
        stack = new_stack
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
