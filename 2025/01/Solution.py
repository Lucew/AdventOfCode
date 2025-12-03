import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append((line[0], int(line[1:])))
    return inputs


def main1():
    result = 0
    inputs = read_input()
    currnum = 50
    for rot, num in inputs:
        if rot == 'L':
            currnum -= num
        else:
            currnum += num
        currnum = currnum % 100
        result += currnum == 0
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0
    inputs = read_input()
    currnum = 50
    for rot, num in inputs:
        turns, num = divmod(num, 100)
        result += turns
        if rot == 'L':
            if num >= currnum and currnum != 0 and num != 0:
                result += 1
            currnum -= num
        else:
            currnum += num
            if currnum >= 100 and num != 0:
                result += 1
        currnum = currnum % 100
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
