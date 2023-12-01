# make a function to read the board
def read_input(path: str = 'input.txt'):
    with open(path) as filet:

        # get the inputs of the game
        inputs = filet.readline()[:-1].split(',')

        # get the boards
        boards = []
        for line in filet.readlines():
            if len(line) == 1:
                # check the dimensions of the board
                if boards:
                    assert len(boards[-1]) == 5 and len(boards[-1][0]) == 5, 'Something is off.'
                boards.append([])
            else:
                boards[-1].append([ele for ele in line[:-1].split(' ') if ele])

    # return boards and inputs
    return boards, inputs


def pretty_print(boards):
    for idx, board in enumerate(boards):
        print()
        print(f'Board {idx+1}:')
        print('---------------')
        for row in board:
            for ele in row:
                print(f'{ele:>3}', end='')
            print()
        print('---------------')


def transform_board(board):
    numbers = dict()
    for rx, row in enumerate(board):
        for cx, ele in enumerate(row):
            assert ele not in numbers, 'Something is off.'
            numbers[ele] = (rx, cx)
    return numbers


def main1():

    # get the inputs and the boards
    boards, inputs = read_input()

    # transform board into set of rows and diagonals
    boards = [[transform_board(board), [0]*5, [0]*5] for board in boards]

    # go through the chosen numbers
    for number in inputs:

        # go through the boards and check the number
        for board in boards:

            # check if it is in there
            if number in board[0]:

                # get the coordinates
                rx, cx = board[0].pop(number)

                # increase the counter of solved elements per row and column
                board[1][rx] += 1
                board[2][cx] += 1

                # check if we are solved
                if board[1][rx] == 5 or board[2][cx] == 5:

                    # sum the things that are left
                    board_sum = sum(int(ele) for ele in board[0].keys())

                    # print the result
                    print(f'Result is: {board_sum*int(number)} for winning number {number} and board sum {board_sum}.')

                    # exit
                    return


def main2():

    # get the inputs and the boards
    boards, inputs = read_input()

    # transform board into set of rows and diagonals
    boards = [[transform_board(board), [0] * 5, [0] * 5] for board in boards]

    # make a set of boards that have won
    won_boards = set()

    # go through the chosen numbers
    for number in inputs:

        # go through the boards and check the number
        for idx, board in enumerate(boards):

            # guard clause for won boards
            if idx in won_boards:
                continue

            # check if it is in there
            if number in board[0]:

                # get the coordinates
                rx, cx = board[0].pop(number)

                # increase the counter of solved elements per row and column
                board[1][rx] += 1
                board[2][cx] += 1

                # check if we are solved
                if board[1][rx] == 5 or board[2][cx] == 5:
                    # sum the things that are left
                    board_sum = sum(int(ele) for ele in board[0].keys())

                    # print the result
                    print(f'Board {idx} won with num {int(number)} and sum {board_sum}. '
                          f'Final score is {int(number)*board_sum}')

                    # add the board to the won boards
                    won_boards.add(idx)


if __name__ == '__main__':
    main1()
    main2()
