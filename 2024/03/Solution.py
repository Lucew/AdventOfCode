from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect
import re


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def main1():

    # make the regex pattern and match it
    pattern = r"mul\(\d{1,3},\d{1,3}\)"
    matches = re.findall(pattern, "".join(read_input()))

    # parse the solution and get the result
    matches = [ele.split(',') for ele in matches]
    result = sum(int(ele[0][4:])*int(ele[1][:-1]) for ele in matches)
    print(f'The result for solution 1 is: {result}')


def main2():

    # make the regex pattern and match it
    pattern = r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't)"
    matches = re.findall(pattern, "".join(read_input()))

    # go through the instructions and resolve the don't
    result = 0
    enabled = True
    for ele in matches:
        if ele.startswith('m') and enabled:
            ele = ele.split(',')
            result += int(ele[0][4:]) * int(ele[1][:-1])
        elif ele == 'do()':
            enabled = True
        else:
            enabled = False
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
