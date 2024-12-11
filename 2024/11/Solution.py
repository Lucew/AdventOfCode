import collections
import functools
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


def read_input(path: str = 'input.txt'):
    with open(path) as filet:
        inputs = list(map(int, filet.read().split()))
    return inputs


def update(stone):
    if stone == 0:
        return [1]
    digits = len(str(stone))
    if digits & 1:
        return [stone * 2024]
    else:
        return divmod(stone, 10 ** (digits // 2))


def main1_old():

    # read the input into memory
    stones = read_input()

    # there is most likely a loop for numbers that start from zero
    for _ in range(25):
        tmp = []
        for stone in stones:
            tmp.extend(update(stone))
        stones = tmp
    print(f'The result for solution 1 is: {len(stones)}')


def main1():
    print(f'The result for solution 1 is: {sum(count_splits(n, 25) for n in read_input())}')


@functools.cache
def count_splits(number, blinks):
    if blinks == 0:
        return 1
    return sum(count_splits(n, blinks - 1) for n in update(number))

def main2():
    print(f'The result for solution 2 is: {sum(count_splits(n, 75) for n in read_input())}')


if __name__ == '__main__':
    main1_old()
    main1()
    main2()
