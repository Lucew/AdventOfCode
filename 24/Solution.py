import collections
from math import lcm

DIRECTIONS = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}


def read_input(path: str = 'input.txt') -> [list[list[str]], set[tuple[int, int, str]]]:
    inputs = []
    blizzards = set()
    with open(path) as filet:
        for rx, line in enumerate(filet.readlines()):

            # strip the line and make it to list
            line = line.rstrip()
            line = list(line)

            # sanity check the borders
            assert line[0] == '#' and line[-1] == '#', f'We are missing row borders in row {rx}.'

            # decrease the positions
            blizzards.update((rx-1, cx-1, ele) for cx, ele in enumerate(line) if ele in DIRECTIONS)
            inputs.append(line)

    # assert start and end at expected position
    assert inputs[0][1] == '.', 'Start not as expected.'
    assert inputs[-1][-2] == '.', 'End not as expected.'

    # assert the board start and end line
    inputs[0][1] = '#'
    inputs[-1][-2] = '#'

    # assert first and last row
    assert all(ele == '#' for ele in inputs[0]), 'First row not as expected.'
    assert all(ele == '#' for ele in inputs[-1]), 'Last row not as expected.'

    return blizzards, len(inputs)-2, len(inputs[0])-2


def get_blizzard_pos(rx: int, cx: int, direction: str, minute: int, row_length: int, column_length: int) -> [int, int]:
    # check the starting positions, apply the offset and take the modulo
    nrx = (rx + DIRECTIONS[direction][0]*minute) % row_length
    ncx = (cx + DIRECTIONS[direction][1]*minute) % column_length
    return nrx, ncx


def blizzard_positions(blizzards: set[tuple[int, int, str]], minute: int, row_length: int, column_length: int) \
        -> dict[tuple[int, int]: list[str]]:
    # go through all blizzards and update their position according to the minute
    new_blizzards = collections.defaultdict(list)
    for rx, cx, direction in blizzards:
        new_blizzards[get_blizzard_pos(rx, cx, direction, minute, row_length, column_length)].append(direction)
    return new_blizzards


def pretty_print(blizzards: dict[tuple[int, int]: list[str]], position: list[int, int],
                 row_length: int, column_length: int,
                 minute: int = 0):

    # build the board
    board = []
    for rx in range(row_length+2):
        # print the first and the last row
        if rx == 0 or rx == row_length + 1:
            board.append(['#']*(column_length+2))
            continue

        # introduce a new row
        row = []
        for cx in range(column_length+2):

            # append the outer barriers
            if cx == 0 or cx == column_length + 1:
                row.append('#')
                continue

            # count the number of blizzards at this place
            position_blizzards = blizzards[(rx-1, cx-1)]

            if position_blizzards:
                symbol = position_blizzards[0] if len(position_blizzards) == 1 else str(len(position_blizzards))
                if rx-1 == position[0] and cx-1 == position[1]:
                    print('We have a blizzard collision.')
            else:
                symbol = '.'

            # append the symbol
            row.append(symbol)

        # append the row to the board
        board.append(row)

    # set the entry and the exit
    board[0][1] = '.'
    board[-1][-2] = '.'

    # set our position
    board[1+position[0]][1+position[1]] = 'x'

    # print the board
    print(f'\n=============== Minute {minute} ===============')
    for row in board:
        for ele in row:
            print(ele, end='')
        print()


def main1():

    # read the input from the file, where positions are in a mxn Matrix
    blizzards, m, n = read_input()

    # estimated cycle start
    estimated_cycle = lcm(m, n)
    print(f'Estimated Cycle is: {estimated_cycle}')

    # sanity check the cycle
    sym_diff = set(blizzard_positions(blizzards, 0, m, n).keys()).symmetric_difference(
        set(blizzard_positions(blizzards, estimated_cycle, m, n).keys()))
    sym_diff2 = set(blizzard_positions(blizzards, 0, m, n).keys()).symmetric_difference(
        set(blizzard_positions(blizzards, estimated_cycle*15, m, n).keys()))
    if sym_diff or sym_diff2:
        raise ValueError('Our initial cycle estimation was wrong.')

    # create all the different cycle states for the blizzard positions
    board_states = dict()
    for minute in range(estimated_cycle):
        board_states[minute] = blizzard_positions(blizzards, minute, m, n)

    # sanity check again
    sym_diff = set(board_states[0].keys()).symmetric_difference({blizzard[:2] for blizzard in blizzards})
    sym_diff2 = set(board_states[122 % estimated_cycle].keys()).symmetric_difference(
        set(blizzard_positions(blizzards, 122 % estimated_cycle, m, n).keys()))
    if sym_diff or sym_diff2:
        raise ValueError('Our cycle could not be proved.')

    # make a bfs
    result = bfs(-1, 0, 0, m, n-1, board_states, estimated_cycle, m, n)
    print(f'The result for solution 1 is: {result}')


def bfs(start_rx, start_cx, start_minute, goal_rx, goal_cx, board_states, estimated_cycle, m, n):

    # make a queue for bfs with our start position
    # the positions in the queue are coded as: (minute, rx, cx)
    queue = collections.deque([(start_minute, start_rx, start_cx)])
    visited = set()
    while queue:

        # pop a position from the queue
        minute, rx, cx = queue.popleft()
        assert not board_states[minute % estimated_cycle][(rx, cx)]

        # check whether we have been at the same position and board state before
        # the board state cycle with the minutes in the estimated cycle length!
        if (minute % estimated_cycle, rx, cx) in visited:
            continue
        else:
            visited.add((minute % estimated_cycle, rx, cx))

        # check whether we can leave (we are at the lower right corner)
        if rx == goal_rx and cx == goal_cx:
            # pretty_print(board_states[minute % estimated_cycle], [rx, cx], m, n, minute)
            return minute

        # get the board state of the next minute to check for free position
        next_state = board_states[(minute + 1) % estimated_cycle]

        # go through the next valid positions (staying at position, left, right, up, down)
        # and check whether they are free in the next state AND are in scope
        for nrx, ncx in [(rx, cx), (rx + 1, cx), (rx - 1, cx), (rx, cx + 1), (rx, cx - 1)]:
            # check whether we are the entry position or leaving position
            # or we are in scope and not a blizzard in the next state
            if (nrx == -1 and ncx == 0) or (nrx == m and ncx == n - 1) or \
                    (0 <= nrx < m and 0 <= ncx < n and not next_state[(nrx, ncx)]):
                queue.append((minute + 1, nrx, ncx))


def main2():
    # read the input from the file, where positions are in a mxn Matrix
    blizzards, m, n = read_input()

    # estimated cycle start
    estimated_cycle = lcm(m, n)

    # create all the different cycle states for the blizzard positions
    board_states = dict()
    for minute in range(estimated_cycle):
        board_states[minute] = blizzard_positions(blizzards, minute, m, n)

    # go to the target
    result = bfs(-1, 0, 0, m, n - 1, board_states, estimated_cycle, m, n)

    # go back to the beginning
    result = bfs(m, n-1, result, -1, 0, board_states, estimated_cycle, m, n)

    # go back to the target
    result = bfs(-1, 0, result, m, n - 1, board_states, estimated_cycle, m, n)
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
