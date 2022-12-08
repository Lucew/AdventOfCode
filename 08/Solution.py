import collections
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append([int(ele) for ele in line])
    return inputs


def main1():
    # get the inputs
    trees = read_input()

    # go through the rows and columns
    can_see = check_rows(trees).union(check_columns(trees))

    # go through the rows and columns
    # got through the matrix and check whether
    print(f'The result for solution 1 is: {len(can_see)}')


def check_rows(matrix):

    # go through all rows
    can_see = set()
    m = len(matrix)
    for rx, row in enumerate(matrix):
        # initialize a max coming from the left and a max coming from the right
        max_left = -1
        max_right = -1

        # go through a row from top and bottom at the same time
        for cx, ele in enumerate(matrix[rx]):
            if ele > max_left:
                can_see.add((rx, cx))
                max_left = ele
            if matrix[rx][-cx-1] > max_right:
                can_see.add((rx, m-cx-1))
                max_right = matrix[rx][-cx-1]
    return can_see


def check_columns(matrix):

    # go through all the columns
    can_see = set()
    n = len(matrix[0])
    for cx in range(n):
        # initialize a max coming from the top and a max coming from the bottom
        max_top = -1
        max_bottom = -1

        for rx in range(len(matrix)):
            if matrix[rx][cx] > max_top:
                can_see.add((rx, cx))
                max_top = matrix[rx][cx]
            if matrix[-rx-1][cx] > max_bottom:
                can_see.add((n-rx-1, cx))
                max_bottom = matrix[-rx-1][cx]

    return can_see


def main2():
    # get the input
    trees = read_input()

    # create a matrix to save the score
    score = [[1]*len(trees[0]) for _ in range(len(trees))]

    # go through the matrix row wise
    score_rows(trees, score)
    score_columns(trees, score)

    # get the maximum score
    result = max(max(row) for row in score)
    print(f'The result for solution 2 is: {result}')


def score_rows(matrix, score):

    # go through all rows
    for rx, row in enumerate(matrix):

        # make a strictly decreasing stack
        stack_left = collections.deque()
        stack_right = collections.deque()

        # go through the row from both directions (can be separated into two loops)
        for cx, ele in enumerate(row):

            # pop from the stack until the stack is empty or the element in there is higher than us
            while stack_left and stack_left[-1][0] < ele:
                stack_left.pop()
            while stack_right and stack_right[-1][0] < row[-cx-1]:
                stack_right.pop()

            # check the distance to the last higher than us and update the score
            score[rx][cx] *= cx - stack_left[-1][1] if stack_left else cx
            score[rx][-cx-1] *= cx - stack_right[-1][1] if stack_right else cx

            # append our tree to the stacks
            stack_left.append((ele, cx))
            stack_right.append((row[-cx-1], cx))


def score_columns(matrix, score):

    # go through all columns
    for cx in range(len(matrix[0])):

        # make a strictly decreasing stack
        stack_top = collections.deque()
        stack_bottom = collections.deque()

        # go through the column from both directions (can be separated into two loops)
        for rx in range(len(matrix)):

            # pop from the stack until the stack is empty or the element in there is higher than us
            while stack_top and stack_top[-1][0] < matrix[rx][cx]:
                stack_top.pop()
            while stack_bottom and stack_bottom[-1][0] < matrix[-rx-1][cx]:
                stack_bottom.pop()

            # check the distance to the last higher than us and update the score
            score[rx][cx] *= rx - stack_top[-1][1] if stack_top else rx
            score[-rx-1][cx] *= rx - stack_bottom[-1][1] if stack_bottom else rx

            # append our tree to the stacks
            stack_top.append((matrix[rx][cx], rx))
            stack_bottom.append((matrix[-rx-1][cx], rx))


if __name__ == '__main__':
    main1()
    main2()
