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

    # go through every line and find first and last number
    result = 0
    for line in read_input():
        nums = [int(ele) for ele in line if ele.isnumeric()]
        result += nums[0]*10 + nums[-1]
    print(f'The result for solution 1 is: {result}')


def main2():

    # the numbers in a list
    nums2int = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

    # make forward and backward strings
    forward = [ele for ele in nums2int.keys()]
    backward = [ele[::-1] for ele in forward]

    # go through each of the lines
    result = 0
    for line in read_input():

        # make forward pass and find digits
        digits = [(idx, int(ele)) for idx, ele in enumerate(line) if ele.isnumeric()]

        # go through the string and find first occurence of numbers
        for num in forward:
            posi = line.find(num)
            if posi != -1:
                digits.append((posi, nums2int[num]))

        # go through the reverse of the line
        line = line[::-1]
        for num in backward:
            posi = line.find(num)
            if posi != -1:
                digits.append((len(line)-posi-len(num), nums2int[num[::-1]]))

        # append to the result
        result += min(digits)[1]*10 + max(digits)[1]

    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    # main1()
    main2()
