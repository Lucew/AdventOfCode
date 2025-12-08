import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    ranges = []
    ingredients = []
    curr_list = ranges
    is_range = True
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            if not line:
                curr_list = ingredients
                is_range = False
                continue
            if is_range:
                curr_list.append(list(int(ele) for ele in line.split('-')))
            else:
                curr_list.append(int(line))
    return ranges, ingredients

def fuse_ranges(ranges: list[list[int, int]]) -> list[list[int, int]]:

    # sort the ranges
    ranges.sort()

    # fuse the ranges
    new_ranges = [ranges[0]]
    for start, end in ranges[1:]:
        if start <= new_ranges[-1][1]:
            new_ranges[-1][1] = max(new_ranges[-1][1], end)
        else:
            new_ranges.append([start, end])
    return new_ranges


def main1():
    result = 0

    # get the ranges and ingredients
    ranges, ingredients = read_input()

    # fuse the ranges
    ranges = fuse_ranges(ranges)

    # go through the ingredients and make binary search
    for ingredient in ingredients:

        # make the binary search
        idx = bisect.bisect_left(ranges, ingredient, key=lambda r: r[0])-1

        # check whether food is fresh
        if 0 <= idx < len(ranges) and ranges[idx][0] <= ingredient <= ranges[idx][1]:
            result += 1

    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # get the ranges and ingredients
    ranges, _ = read_input()

    # fuse the ranges
    ranges = fuse_ranges(ranges)

    # go through the ranges once more
    for start, end in ranges:
        result += (end - start)+1
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
