import collections
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


def check_mirror_axis(equal_idx, gx=0):
    found = False
    mirror_axis = 1
    max_idx = max(equal_idx.keys())
    for mirror_axis in range(1, max_idx+1):

        # check whether it is a mirror axis
        left = mirror_axis - 1
        right = mirror_axis
        found = True
        while left >= 0 and right <= max_idx:
            if right not in equal_idx[left]:
                found = False
                break
            left -= 1
            right += 1

        # terminate if we found one
        if found:
            break
    return mirror_axis if found else -1


def main1():
    result = 0

    # get the input and put into groups
    lines = read_input()
    groups = [[]]
    for line in lines:
        if line:
            groups[-1].append(line)
        else:
            groups.append([])

    # we could hash each row and column that is equal and then check for symmetries
    for gx, group in enumerate(groups):

        # make hashes for equal rows and columns
        row_hashes = collections.defaultdict(list)
        col_hashes = collections.defaultdict(list)

        # collect hashes for rows and columns
        cols = [[] for _ in range(len(group[0]))]
        for rx, line in enumerate(group):
            row_hashes[line].append(rx)
            for cx, ele in enumerate(line):
                cols[cx].append(ele)
        for cx, col in enumerate(cols):
            col_hashes["".join(col)].append(cx)

        # change the notation of the hashes
        equal_rows = collections.defaultdict(set)
        for values in row_hashes.values():
            for val in values:
                equal_rows[val].update(oval for oval in values if oval != val)
        equal_cols = collections.defaultdict(set)
        for values in col_hashes.values():
            for val in values:
                equal_cols[val].update(oval for oval in values if oval != val)

        # check the horizontal possibilities
        hor = check_mirror_axis(equal_rows, gx)
        if hor != -1:
            result += 100*hor
            continue

        # check the vertical possibilities
        vert = check_mirror_axis(equal_cols, gx)
        if vert != -1:
            result += vert
            continue
        raise ValueError(f"Did not find any mirror axis for group {gx}.")

    print(f'The result for solution 1 is: {result}')


def check_axis_diff_smudged(group, gx):

    # compute the diffs between all the axis
    diffs = {(up, down): sum(ele1 != ele2 for ele1, ele2 in zip(row1, row2))
             for up, row1 in enumerate(group) for down, row2 in enumerate(group[up+1:], up+1)}

    # go through each of the mirror axis and check for diff
    final_axis = -1
    for mirror_axis in range(1, len(group)):

        # check whether it is a mirror axis
        up = mirror_axis - 1
        down = mirror_axis
        diff = 0
        while up >= 0 and down < len(group):
            diff += diffs[(up, down)]
            if diff > 1:
                break
            up -= 1
            down += 1

        # check whether we found exactly one diff
        if diff == 1:
            final_axis = mirror_axis
            break
    return final_axis


def main2():
    result = 0

    # get the input and put into groups
    lines = read_input()
    groups = [[]]
    for line in lines:
        if line:
            groups[-1].append(line)
        else:
            groups.append([])

    # we could hash each row and column that is equal and then check for symmetries
    for gx, group in enumerate(groups):

        # check the horizontal possibilities
        hor = check_axis_diff_smudged(group, gx)
        if hor != -1:
            result += 100 * hor
            continue

        # transpose the group (rows become columns)
        cols = ["".join(row[cx] for row in group) for cx in range(len(group[0]))]

        # check the vertical possibilities
        vert = check_axis_diff_smudged(cols, gx)
        if vert != -1:
            result += vert
            continue
        raise ValueError(f"Did not find any mirror axis for group {gx}.")
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
