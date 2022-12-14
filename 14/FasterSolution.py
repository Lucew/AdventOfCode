from collections import defaultdict
from sortedcontainers import SortedList


"""
Spent way too much time overthinking all other solutions.
NormalThinkingSolution is the feasible one.

"""

"""
------------------------------------------------
| Function names       | Minimum runtime in ms |
------------------------------------------------
| Solution.main1       | 50.69 (+0.00)         |
| FasterSolution.main1 | 55.68 (+4.99)         |
| FasterSolution.main2 | 2205.64 (+2149.97)    |
| Solution.main2       | 7699.24 (+5493.60)    |
------------------------------------------------
"""


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
    blocked = defaultdict(SortedList)
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

        # make a sand corn
        rx, cx = 0, 500

        # get the end position
        while True:

            # get the index of a row bigger than ours
            min_idx = blocked[cx].bisect_right(rx)

            # check the current column for the minimal row
            if min_idx == len(blocked[cx]):
                print(f'The result for solution 1 is: {units}')
                return
            else:
                rx = blocked[cx][min_idx] - 1

            # check whether we can slide to the left
            if cx-1 in blocked and rx+1 not in blocked[cx-1]:
                rx = rx+1
                cx = cx-1
                continue

            # check whether we can slide to the right
            elif cx + 1 in blocked and rx + 1 not in blocked[cx + 1]:
                rx = rx + 1
                cx = cx + 1
                continue

            # check whether we fall into the abyss
            elif cx-1 not in blocked or cx+1 not in blocked:
                print(f'The result for solution 1 is: {units}')
                return
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
    blocked = defaultdict(lambda: SortedList([highest_row+2]))
    for line in inputs:

        # go through all points
        for start, end in zip(line[:-1], line[1:]):

            # check whether it is a vertical or horizontal line
            if start[0] == end[0]:  # vertical
                for rx in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                    if rx not in blocked[start[0]]:
                        blocked[start[0]].add(rx)
            elif start[1] == end[1]:  # horizontal
                for cx in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                    if start[1] not in blocked[cx]:
                        blocked[cx].add(start[1])
            else:
                raise NotImplementedError

    # let the sand fall!
    units = 0
    while True:

        # make a sand corn
        rx, cx = 0, 500

        # get the end position
        while True:

            # check the current column and find the highest row we land on
            rx = blocked[cx][blocked[cx].bisect_right(rx)] - 1

            # slide to the right
            if rx+1 not in blocked[cx-1]:
                rx = rx + 1
                cx = cx - 1
                continue

            # slide to the left
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
