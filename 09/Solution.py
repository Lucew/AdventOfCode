from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip().split(' ')
            inputs.append([line[0], int(line[1])])
    return inputs


def main1():

    # read the input
    inputs = read_input()

    # make two pointers for head and tail
    head = [0, 0]
    tail = [0, 0]

    # make a direction dict
    directions = {'R': (0, 1), 'L': (0, -1), 'U': (1, 0), 'D': (-1, 0)}

    # make a set to keep visited positions
    visited = set()

    for direction, steps in inputs:
        direction = directions[direction]
        for _ in range(steps):

            # update the head pointer
            head[0] += direction[0]
            head[1] += direction[1]

            # update the tail
            update_knot(head, tail)

            # append the new position to the seen one
            visited.add((tail[0], tail[1]))
    print(f'The result for solution 1 is: {len(visited)}')


def update_knot(head, tail):

    # calculate the distances between each of the node
    # vertical distance
    vertical = head[0] - tail[0]
    # horizontal distance
    horizontal = head[1] - tail[1]

    # The reasoning for this logic is heavily merged down.
    # One can try to come up with it by drawing a picture
    # of the 16 positions the head can be if the tail
    # needs to be moved and then check for the conditions.
    #
    # Look at the picture in the repo if you want to
    # understand them better.

    # make the checks for updating
    if vertical == 0 and abs(horizontal) > 1:  # only horizontal movement
        # update the horizontal position but only max one
        tail[1] += 1 if horizontal > 0 else -1
    elif horizontal == 0 and abs(vertical) > 1:
        tail[0] += 1 if vertical > 0 else -1
    elif abs(horizontal) > 1 or abs(vertical) > 1:
        # move horizontal and vertical
        tail[0] += 1 if vertical > 0 else -1
        tail[1] += 1 if horizontal > 0 else - 1


def main2():

    # read the input
    inputs = read_input()

    # make a list of position for every knots in the rope
    knots = [[0]*2 for _ in range(10)]

    # make a direction dict
    directions = {'R': (0, 1), 'L': (0, -1), 'U': (1, 0), 'D': (-1, 0)}

    # make a set to keep visited positions
    visited = set()

    for direction, steps in inputs:
        direction = directions[direction]
        for _ in range(steps):

            # update the head pointer
            knots[0][0] += direction[0]
            knots[0][1] += direction[1]

            # go through all the knots one by one
            for idx, knot in enumerate(knots[1:]):
                # update the knot looking at the previous one
                update_knot(knots[idx], knot)

            # append the new position of the tail
            visited.add((knots[-1][0], knots[-1][1]))
    print(f'The result for solution 2 is: {len(visited)}')


if __name__ == '__main__':
    main1()
    main2()
