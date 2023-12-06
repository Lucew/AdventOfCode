from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect
from math import sqrt, ceil, floor


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def calculate_borders(target_distance: int, time: int):

    # calculate the square root once
    sqrt_val = sqrt(time**2-4*target_distance)

    # calculate both borders and then add them to round numbers
    left_border = floor((-time + sqrt_val)/(-2))+1
    right_border = ceil((-time - sqrt_val)/(-2))-1
    return left_border, right_border


def calculate_possibilities(target_distance: int, time: int):
    left, right = calculate_borders(target_distance, time)
    return right-left+1


def main1():

    # it is a quadratic formula since it originates from
    # d = x*(t-x) = x*t - x^2 > c
    #
    # When we solve it we get to
    #
    # h_1 = ((-t) + sqrt(t^2-4c))/(-2)
    # h_2 = ((-t) - sqrt(t^2-4c))/(-2)
    # h_1 < x_s < h_2

    lines = read_input()
    times = [int(ele) for ele in lines[0].split(" ")[1:] if ele]
    distances = [int(ele) for ele in lines[1].split(" ")[1:] if ele]

    result = 1
    for dist, time in zip(distances, times):
        result *= calculate_possibilities(dist, time)

    print(f'The result for solution 1 is: {result}')


def main2():

    # get the input
    lines = read_input()
    times = [ele for ele in lines[0].split(" ")[1:] if ele]
    distances = [ele for ele in lines[1].split(" ")[1:] if ele]

    # put it into a number
    time = int("".join(times))
    distance = int("".join(distances))
    result = calculate_possibilities(distance, time)

    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
