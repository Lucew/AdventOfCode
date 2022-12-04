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

    # get the input from the file
    lines = read_input()

    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # get the input from the file
    lines = read_input()

    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
