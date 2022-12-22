import collections
import re
from bisect import bisect


def read_input(path: str = 'input.txt'):
    col_blocked = collections.defaultdict(list)
    row_blocked = collections.defaultdict(list)
    col_open = collections.defaultdict(list)
    row_open = collections.defaultdict(list)
    walk_path = ""
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
                if ele == '.':
                    col_open[cx].append(rx)
                    row_open[rx].append(cx)
                elif ele == '#':
                    col_blocked[cx].append(rx)
                    row_blocked[rx].append(cx)

    return row_open, col_open, row_blocked, col_blocked, walk_path


def make_step(instruction: str, position: list[int, int, str], turning: dict[str: dict[str: str], str: dict[str: str]],
              row_open: dict[int: list[int]], col_open: dict[int: list[int]],
              row_blocked: dict[int: list[int]], col_blocked: dict[int: list[int]]):

    # check row or col depending on the direction we are facing
    if position[2] == '>' or position[2] == '<':
        pass
    elif position[2] == '^' or position[2] == 'v':
        pass
    else:
        raise NotImplementedError


def check_path(position, steps, free: list[int], blocked: list[int]):

    # trivial case
    if not position:
        return position

    # get the minimum and maximum point (to calculate the length of this row/col)
    min_coord = min(free[0] if free else -1, blocked[0] if blocked else -1)
    max_coord = min(free[-1] if free else float('inf'), blocked[-1] if blocked else float('inf'))
    row_length = max_coord - min_coord + 1

    # check whether we will wrap around and get our new position (in relation to starting point)
    wraps, relative_posi = divmod(position + steps, row_length)

    # check whether anything is blocked in our line
    if not blocked:
        return relative_posi + min_coord

    # something in our way is blocked
    else:
        # bisect the blocked list in order to check for the next block
        blocked_idx = bisect(blocked, position)

        # if we go to the smaller indices (left for row or up for column), we will hit either the blocked element
        # to the left/up of us, or we hit the highest element
        if steps < 0:

            # lets check whether there is an element smaller than us in the sorted list
            if blocked_idx-1 > 0:

                # there is an element smaller than us, so we return us right of it or our - steps position
                return max(blocked[blocked_idx] + 1, )
            else:
                blocked[-1]


def multiply_list(max_position, ):



def main1():

    # get the input readings
    row_open, col_open, row_blocked, col_blocked, path = read_input()

    # extract the commands from the path
    path = re.findall(r'[0-9]*[A-Z]', path)
    max_steps = max(int(ele[:-1]) for ele in path)

    # multiply the list for easy binary search for the next collision


    # turning dict for quick turning
    turning = {'R': {'>': 'v', '<': '^', 'v': '<', '^': '>'}, 'L': {'>': '^', '<': 'v', 'v': '>', '^': '<'}}

    # go through the maze
    position = [0, row_open[0][0], '>']
    print(max_steps)
    for command in path:

        pass

    result = 0
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
