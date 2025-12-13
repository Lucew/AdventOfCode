import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    inputs = [[]]
    with open(path) as filet:
        for line in filet.readlines():
            print('ll', line, len(line))
            if len(line) == 1:
                inputs.append(list())
            elif line[-2] == ':':
                continue
            else:
                line = line.rstrip()
                inputs[-1].append(line)
    return inputs


def main1():
    result = 0

    # get the inputs
    inputs = read_input()

    # go through the presents and check whether they can fit
    for area in inputs[-1]:

        # get the area
        area, pieces = area.split(': ')
        pieces = [int(ele) for ele in pieces.split(' ')]
        area = [int(ele) for ele in area.split('x')]
        result += sum(pieces)*9 <= area[0]*area[1]
    # LOL, did not think this is the solutions
    # just tried for fun
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
