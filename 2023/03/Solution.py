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

    # make a scan to find the positions of symbols
    valid = {tupled
             for rx, row in enumerate(read_input())
             for cx, ele in enumerate(row)
             for tupled in [(rx-1, cx), (rx+1, cx), (rx, cx-1), (rx, cx+1),
                            (rx-1, cx+1), (rx+1, cx-1), (rx-1, cx-1), (rx+1, cx+1)]
             if not ele.isnumeric() and ele != '.'}

    # make a second scan through the rows and find numbers and check whether they are valid
    result = 0
    for rx, line in enumerate(read_input()):
        cx = 0
        while cx < len(line):

            # check whether we hit a number
            currnum = 0
            currvalid = False
            while cx < len(line) and line[cx].isnumeric():
                currnum = currnum*10 + int(line[cx])
                if (rx, cx) in valid:
                    currvalid = True
                cx += 1

            # add the number if valid
            if currvalid:
                result += currnum
            cx += 1
    print(f'The result for solution 1 is: {result}')


def main2():
    # make a scan to find the positions of symbols
    valid = {tupled: (rx, cx)
             for rx, row in enumerate(read_input())
             for cx, ele in enumerate(row)
             for tupled in [(rx - 1, cx), (rx + 1, cx), (rx, cx - 1), (rx, cx + 1),
                            (rx - 1, cx + 1), (rx + 1, cx - 1), (rx - 1, cx - 1), (rx + 1, cx + 1)]
             if ele == '*'}
    found_nums = {tupled: [] for tupled in valid.values()}

    # make a second scan and find all valid numbers and put them to each gear
    for rx, line in enumerate(read_input()):
        cx = 0
        while cx < len(line):

            # check whether we hit a number and it is next to a gear
            currnum = 0
            nextto = set()
            while cx < len(line) and line[cx].isnumeric():
                currnum = currnum * 10 + int(line[cx])
                if (rx, cx) in valid:
                    nextto.add(valid[(rx, cx)])
                cx += 1

            # add the number to gears if we have any
            for nrx, ncx in nextto:
                found_nums[(nrx, ncx)].append(currnum)
            cx += 1

    # compute the gear things
    result = 0
    for _, nums in found_nums.items():
        if len(nums) == 2:
            result += nums[0]*nums[1]
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
