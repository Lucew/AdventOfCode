from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def main1():
    result = 0
    for line in read_input():

        # get the numbers into a list
        nums = [int(ele) for ele in line.split(" ")]

        # save the last number
        last_num = [nums[-1]]

        # now shrink the values
        while any(ele != 0 for ele in nums):

            # get the new nums
            nums = [b-a for a, b in zip(nums[:-1], nums[1:])]

            # save the last number
            last_num.append(nums[-1])

        # now compute up high
        adder = 0
        for num in reversed(last_num):
            adder = num+adder
        result += adder

    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0
    for line in read_input():

        # get the numbers into a list
        nums = [int(ele) for ele in line.split(" ")]

        # save the last number
        first_num = [nums[0]]

        # now shrink the values
        while any(ele != 0 for ele in nums):
            # get the new nums
            nums = [b - a for a, b in zip(nums[:-1], nums[1:])]

            # save the last number
            first_num.append(nums[0])

        # now compute down low
        adder = 0
        for num in reversed(first_num):
            adder = num-adder
        result += adder
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
