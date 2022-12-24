import collections


DIRECTIONS = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}


def read_input(path: str = 'input.txt') -> [list[list[str]], set[tuple[int, int, str]]]:
    inputs = []
    blizzards = set()
    with open(path) as filet:
        for rx, line in enumerate(filet.readlines()):
            line = line.rstrip()
            line = list(line)
            blizzards.update((rx, cx, ele) for cx, ele in enumerate(line) if ele in DIRECTIONS)
            inputs.append()
    return inputs, blizzards


def get_new_blizzard_pos(rx: int, cx: int, direction: str, board: list[list[str]]) -> [int, int]:
    # check the direction and update accordingly
    nrx = rx + DIRECTIONS[direction][0]
    ncx = cx + DIRECTIONS[direction][1]

    # check whether we hit at wall
    if board[nrx][ncx] == '#':
        if direction == '>':
            ncx = 1
        elif direction == '<':
            ncx = len(board) - 2
        elif direction == '^':
            nrx = len(board[0]) - 2
        elif direction == 'v':
            nrx = 1
        else:
            # Sanity checking
            raise NotImplementedError
    return nrx, ncx


def update_blizzards(board: list[list[str]], blizzards: set[tuple[int, int, str]]):
    # make a new blizzards set
    new_blizzards = set()
    for rx, cx, direction in blizzards:

        # get net blizzard position to check whether we need to reset
        nrx, ncx = get_new_blizzard_pos(rx, cx, direction, board)

        # assert that we never hit our position (should never happen, just sanity checking)
        assert board[nrx][ncx] != 'x', 'Blizzard hit us (should not happen).'

        # remove the old symbol
        if board[rx][cx] in DIRECTIONS:
            board[rx][cx] = '.'
        elif board[rx][cx].isnumeric():
            new_number = int(board[rx][cx])-1
            board[rx][cx] = str(new_number) if new_number else '.'
        elif board[rx][cx] == '.':
            board[rx][cx] = direction

        # update the set
        new_blizzards.add((nrx, ncx, direction))

        # set the new symbol
        if board[nrx][ncx] in DIRECTIONS:
            board[nrx][ncx] = '2'
        elif board[nrx][ncx].isnumeric():
            board[nrx][ncx] = str(int(board[nrx][ncx])+1)
        elif board[nrx][ncx] == '.':
            board[nrx][ncx] = direction
    return new_blizzards

def main1():

    # read the input from the file
    inputs, blizzards = read_input()

    # make a queue for bfs
    result = 0
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
