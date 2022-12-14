from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append([(int(coords.split(',')[0]), int(coords.split(',')[1])) for coords in line.split(' -> ')])
    return inputs


def main1():

    # read the input
    inputs = read_input()

    # extend the input to have blocked blocks
    blocked = defaultdict(set)
    for line in inputs:

        # go through all points
        for start, end in zip(line[:-1], line[1:]):

            # check whether it is a vertical or horizontal line
            if start[0] == end[0]:  # vertical
                for rx in range(min(start[1], end[1]), max(start[1], end[1])+1):
                    blocked[start[0]].add(rx)
            elif start[1] == end[1]:  # horizontal
                for cx in range(min(start[0], end[0]), max(start[0], end[0])+1):
                    blocked[cx].add(start[1])
            else:
                raise NotImplementedError

    # let the sand fall!
    units = 0
    while True:

        # make a sandcorn
        rx, cx = 0, 500

        # get the end position
        while True:

            # get all the rows bigger than our current
            blocked_rx = [ele for ele in blocked[cx] if ele > rx]

            # check the current column for the minimal row
            if cx not in blocked or not blocked_rx:
                print(f'The result for solution 1 is: {units}')
                return
            else:
                rx = min(blocked_rx) - 1

            # check whether we can slide to the left
            if cx-1 not in blocked:
                print(f'The result for solution 1 is: {units}')
                return
            else:

                # check for the element to the left to be existing
                if rx+1 not in blocked[cx-1]:
                    rx = rx+1
                    cx = cx-1
                    continue

            # check whether we can slide to the right
            if cx + 1 not in blocked:
                print(f'The result for solution 1 is: {units}')
                return
            else:

                # check for the element to the left to be existing
                if rx + 1 not in blocked[cx + 1]:
                    rx = rx + 1
                    cx = cx + 1
                    continue

            # we cannot slide further
            blocked[cx].add(rx)
            units += 1
            break


def main2():

    # read the input
    inputs = read_input()

    # get the highest row number of all the scans
    highest_row = max(ele[1] for line in inputs for ele in line)

    # extend the input to have blocked blocks. Also block the row eleven by default
    blocked = defaultdict(lambda: {highest_row+2})
    for line in inputs:

        # go through all points
        for start, end in zip(line[:-1], line[1:]):

            # check whether it is a vertical or horizontal line
            if start[0] == end[0]:  # vertical
                for rx in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                    blocked[start[0]].add(rx)
            elif start[1] == end[1]:  # horizontal
                for cx in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                    blocked[cx].add(start[1])
            else:
                raise NotImplementedError

    # let the sand fall!
    units = 0
    while True:

        # make a sandcorn
        rx, cx = 0, 500

        # get the end position
        while True:

            # get all the rows bigger than our current
            blocked_rx = [ele for ele in blocked[cx] if ele > rx]

            # check the current column and find the highest row we land on
            rx = min(blocked_rx) - 1

            if rx+1 not in blocked[cx-1]:
                rx = rx + 1
                cx = cx - 1
                continue
            elif rx+1 not in blocked[cx+1]:
                rx = rx + 1
                cx = cx + 1
                continue

            # we can not slide further
            # put our sand into the blocked dict
            blocked[cx].add(rx)

            # update the units
            units += 1

            # check for end condition
            if (rx, cx) == (0, 500):
                print(f'The result for solution 2 is: {units}')
                return
            break


if __name__ == '__main__':
    main1()
    main2()
