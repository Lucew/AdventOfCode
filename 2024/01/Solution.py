import collections
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(tuple(map(int, line.split('   '))))
    return inputs


def main1():
    result = 0

    # get the numbers
    numbers = read_input()

    # split the numbers
    n1, n2 = zip(*numbers)

    # compute the result
    result = sum(abs(ele1-ele2) for ele1, ele2 in zip(sorted(n1), sorted(n2)))

    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # get the numbers
    numbers = read_input()

    # split the numbers
    n1, n2 = zip(*numbers)

    # count in the right list
    cn2 = collections.Counter(n2)
    result = sum(ele*cn2[ele] for ele in n1)
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
