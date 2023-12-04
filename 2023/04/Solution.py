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

    def parse_set(setstr: str) -> set[int]:
        return set(int(num) for num in setstr.split(" ") if num)

    # go through the lines and make a set intersection
    for line in read_input():

        # parse the line into the two sets
        _, sets = line.split(": ")

        # get the two different sets
        winset, haveset = sets.split(" | ")

        # make a set of numbers we have and of winning numbers
        winset = parse_set(winset)
        haveset = parse_set(haveset)

        # check the intersection
        combset = winset & haveset

        # check whether we have some winning numbers
        if combset:
            result += 1 << (len(combset)-1)
    print(f'The result for solution 1 is: {result}')


def main2():

    def parse_set(setstr: str) -> set[int]:
        return set(int(num) for num in setstr.split(" ") if num)

    # go through the lines and make a set intersection
    inputs = read_input()
    cards = [1]*len(inputs)
    for cdx, line in enumerate(inputs):

        # parse the line into the two sets
        _, sets = line.split(": ")

        # get the two different sets
        winset, haveset = sets.split(" | ")

        # make a set of numbers we have and of winning numbers
        winset = parse_set(winset)
        haveset = parse_set(haveset)

        # check the intersection
        combset = winset & haveset

        # check whether we have some winning numbers
        for ndx in range(1, len(combset)+1):
            cards[cdx+ndx] += cards[cdx]

    print(f'The result for solution 2 is: {sum(cards)}')


if __name__ == '__main__':
    main1()
    main2()
