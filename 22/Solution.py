import re
import collections
import math


def read_input(path: str = 'input.txt'):
    walk_path = ""
    free = set()
    blocked = set()
    row_minmax = collections.defaultdict(lambda: [math.inf, -1])
    col_minmax = collections.defaultdict(lambda: [math.inf, -1])

    with open(path) as filet:
        next_path = False
        for rx, line in enumerate(filet.readlines()):

            # read the line
            line = line.rstrip()

            if next_path:
                walk_path = line

            # check if it is empty line
            if not line:
                next_path = True

            # go through each element and append to the
            # right dict
            for cx, ele in enumerate(line):
                # update the min max of the rows and columns
                if ele == '#' or ele == '.':
                    # update the minima
                    row_minmax[rx][0] = min(row_minmax[rx][0], cx)
                    col_minmax[cx][0] = min(col_minmax[cx][0], rx)

                    # update the maxima
                    row_minmax[rx][1] = max(row_minmax[rx][1], cx)
                    col_minmax[cx][1] = max(col_minmax[cx][1], rx)

                # update the two sets of occupied or free positions
                if ele == '.':
                    free.add((rx, cx))
                elif ele == '#':
                    blocked.add((rx, cx))

    return free, blocked, walk_path, row_minmax, col_minmax


def next_position(rx: int, cx: int, direction: str,
                  row_minmax: dict[int: list[int, int]], col_minmax: dict[int: list[int, int]]):

    # calculate the new position based on the direction
    if direction == '>':
        cx += 1
        # check whether we wrapped around
        if cx > row_minmax[rx][1]:
            cx = row_minmax[rx][0]
    elif direction == '<':
        cx -= 1
        # check whether we wrapped around
        if cx < row_minmax[rx][0]:
            cx = row_minmax[rx][1]
    elif direction == '^':
        rx -= 1
        # check whether we wrapped around
        if rx < col_minmax[cx][0]:
            rx = col_minmax[cx][1]
    elif direction == 'v':
        rx += 1
        # check whether we wrapped around
        if rx > col_minmax[cx][1]:
            rx = col_minmax[cx][0]
    else:
        raise NotImplementedError
    return rx, cx


def main1():

    # get the input readings
    free, blocked, path, row_minmax, col_minmax = read_input()

    # extract the commands from the path
    path = re.findall(r'[0-9]*[A-Z]', path + 'A')

    # turning dict for quick turning
    turning = {'R': {'>': 'v', '<': '^', 'v': '<', '^': '>'}, 'L': {'>': '^', '<': 'v', 'v': '>', '^': '<'},
               'A': {'>': '>', '<': '<', 'v': 'v', '^': '^'}}

    # find the starting point
    start = row_minmax[0][0]
    while (0, start) in blocked:
        start += 1

    # go through the maze
    position = [0, start, '>']
    for command in path:

        # get the amount of steps
        steps = int(command[:-1])

        # make the steps
        for step in range(steps):

            # get the new position
            rx, cx = next_position(*position, row_minmax, col_minmax)

            # check whether the way is blocked
            if (rx, cx) in blocked:
                break

            # check whether we can go there
            elif (rx, cx) in free:
                position[0] = rx
                position[1] = cx

        # make the rotation
        position[2] = turning[command[-1]][position[2]]

    # make a dict for value translation of the direction
    value = {'>': 0, '<': 2, 'v': 1, '^': 3}
    print(position)

    result = 1000*(position[0]+1) + 4*(position[1]+1) + value[position[2]]
    print(f'The result for solution 1 is: {result}')


def wrap_around(rx: int, cx: int, direction: str,
                row_minmax: dict[int: list[int, int]], col_minmax: dict[int: list[int, int]], lenght=50):

    # calculate the new position based on the direction
    if direction == '>':
        cx += 1
        # check whether we wrapped around
        if cx > row_minmax[rx][1]:

            if rx < 50:
                cx = 99
                rx = 149 - rx
                direction = '<'
            elif rx < 100:
                cx = rx + 50
                rx = 49
                direction = '^'
            elif rx < 150:
                cx = 149
                rx = 149 - rx
                direction = '<'
            elif rx < 200:
                cx = rx - 100
                rx = 149
                direction = '^'
            else:
                raise NotImplementedError
    elif direction == '<':
        cx -= 1
        # check whether we wrapped around
        if cx < row_minmax[rx][0]:

            if rx < 50:
                cx = 0
                rx = 149 - rx
                direction = '>'
            elif rx < 100:
                cx = rx - 50
                rx = 100
                direction = 'v'
            elif rx < 150:
                cx = 50
                rx = 149-rx
                direction = '>'
            elif rx < 200:
                cx = rx - 100
                rx = 0
                direction = 'v'
            else:
                raise NotImplementedError
    elif direction == '^':
        rx -= 1
        # check whether we wrapped around
        if rx < col_minmax[cx][0]:

            if cx < 50:
                rx = 50 + cx
                cx = 50
                direction = '>'
            elif cx < 100:
                rx = cx + 100
                cx = 0
                direction = '>'
            elif cx < 150:
                rx = 199
                cx = cx - 100
                direction = '^'
            else:
                raise NotImplementedError
    elif direction == 'v':
        rx += 1
        # check whether we wrapped around
        if rx > col_minmax[cx][1]:
            if cx < 50:
                cx = cx + 100
                rx = 0
                direction = 'v'
            elif cx < 100:
                rx = cx + 100
                cx = 49
                direction = '<'
            elif cx < 150:
                rx = cx - 50
                cx = 99
                direction = '<'
            else:
                raise NotImplementedError
    else:
        raise NotImplementedError
    return rx, cx, direction


def main2():

    # get the input readings
    free, blocked, path, row_minmax, col_minmax = read_input()

    # extract the commands from the path
    path = re.findall(r'[0-9]*[A-Z]', path + 'A')

    # turning dict for quick turning
    turning = {'R': {'>': 'v', '<': '^', 'v': '<', '^': '>'}, 'L': {'>': '^', '<': 'v', 'v': '>', '^': '<'},
               'A': {'>': '>', '<': '<', 'v': 'v', '^': '^'}}

    # find the starting point
    start = row_minmax[0][0]
    while (0, start) in blocked:
        start += 1

    # go through the maze
    position = [0, start, '>']
    for command in path:

        # get the amount of steps
        steps = int(command[:-1])

        # make the steps
        for step in range(steps):

            # get the new position
            rx, cx, direction = wrap_around(*position, row_minmax, col_minmax)

            # check whether the way is blocked
            if (rx, cx) in blocked:
                break

            # check whether we can go there
            elif (rx, cx) in free:
                position[0] = rx
                position[1] = cx
                position[2] = direction

            else:
                print(rx, cx)
                raise ValueError


        # make the rotation
        position[2] = turning[command[-1]][position[2]]

    # make a dict for value translation of the direction
    value = {'>': 0, '<': 2, 'v': 1, '^': 3}
    print(position)

    result = 1000 * (position[0] + 1) + 4 * (position[1] + 1) + value[position[2]]
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
