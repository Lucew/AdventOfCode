import collections
import heapq
import functools
import bisect
from linecache import cache


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def recursive_start(num: str, digits: int):

    # make the memoized function
    @functools.cache
    def recursion(idx: int, k: int):
        if k == 0:
            return 0
        if len(num)-idx == k:
            return int(num[-k:])
        return max(int(num[idx])*10**(k-1) + recursion(idx+1, k-1), recursion(idx+1, k))

    return recursion(0, digits)



def main1():
    result = 0
    inputs = read_input()
    for line in inputs:
        res = recursive_start(line, 2)
        result += res
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0
    inputs = read_input()
    for line in inputs:
        res = recursive_start(line, 12)
        result += res
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
