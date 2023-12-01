from collections import defaultdict
"""
Spent way too much time overthinking all other solutions.
This should be the one.

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
    blocked = set()
    for line in inputs:

        # go through all points
        for start, end in zip(line[:-1], line[1:]):

            # check whether it is a vertical or horizontal line
            if start[0] == end[0]:  # vertical
                for rx in range(min(start[1], end[1]), max(start[1], end[1])+1):
                    blocked.add((rx, start[0]))
            elif start[1] == end[1]:  # horizontal
                for cx in range(min(start[0], end[0]), max(start[0], end[0])+1):
                    blocked.add((start[1], cx))
            else:
                raise NotImplementedError

    # get the highest row number of all the scans
    highest_row = max(ele[0] for ele in blocked)

    # let the sand fall!
    units = 0
    while True:

        # make a sand corn
        rx, cx = 0, 500

        # simulate the fall
        while True:

            # check if we can fall down
            can_fall = False
            for nrx, ncx in [(rx+1, cx), (rx+1, cx-1), (rx+1, cx+1)]:

                # check whether we can fall deeper in the current column
                if (nrx, ncx) not in blocked:
                    can_fall = True
                    rx, cx = nrx, ncx
                    break

            # make our end condition check
            if rx >= highest_row:
                print(f'The result for solution 1 is: {units}')
                return

            # block another field if cannot fall deeper
            if not can_fall:
                blocked.add((rx, cx))
                units += 1
                break


def main2():

    # read the input
    inputs = read_input()

    # extend the input to have blocked blocks
    blocked = set()
    for line in inputs:

        # go through all points
        for start, end in zip(line[:-1], line[1:]):

            # check whether it is a vertical or horizontal line
            if start[0] == end[0]:  # vertical
                for rx in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                    blocked.add((rx, start[0]))
            elif start[1] == end[1]:  # horizontal
                for cx in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                    blocked.add((start[1], cx))
            else:
                raise NotImplementedError

    # get the highest row number of all the scans
    highest_row = max(ele[0] for ele in blocked) + 2

    # let the sand fall!
    units = 0
    while True:

        # make a sand corn
        rx, cx = 0, 500

        # simulate the fall
        while True:

            # check if we can fall down
            can_fall = False
            for nrx, ncx in [(rx + 1, cx), (rx + 1, cx - 1), (rx + 1, cx + 1)]:

                # check whether we can fall deeper in the current column
                if (nrx, ncx) not in blocked:
                    can_fall = True
                    rx, cx = nrx, ncx
                    break

            # block another field if cannot fall deeper
            if not can_fall or rx == highest_row - 1:
                blocked.add((rx, cx))

                units += 1

                # make our end condition check
                if (rx, cx) == (0, 500):
                    print(f'The result for solution 2 is: {units}')
                    return

                break


if __name__ == '__main__':
    main1()
    main2()
