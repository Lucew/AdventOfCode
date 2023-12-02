import functools
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def main1():
    result = 0

    # save the different colors and their participation
    available = {"red": 12, "green": 13, "blue": 14}

    # go through the lines and check whether the game is valid
    for line in read_input():

        # get the game
        game, patches = line.split(": ")
        game = int(game.split(" ")[1])

        # keep track whether it is valid
        valid = True

        # get the patches
        patches = patches.split("; ")
        for patch in patches:
            if not valid:
                break
            colors = patch.split(", ")
            for color in colors:
                if not valid:
                    break
                number, color = color.split(" ")
                if int(number) > available[color]:
                    valid = False
                    break

        # check whether we need to add
        if valid:
            result += game

    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # go through the lines and check whether the game is valid
    for line in read_input():

        # get the game
        game, patches = line.split(": ")
        game = int(game.split(" ")[1])

        # save the different colors and their maximum
        available = {"red": 0, "green": 0, "blue": 0}

        # get the patches
        patches = patches.split("; ")
        for patch in patches:
            colors = patch.split(", ")
            for color in colors:
                number, color = color.split(" ")
                available[color] = max(int(number), available[color])

        # get the multiplication of all the numbers
        result += functools.reduce(lambda x, y: x*y, available.values())
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
