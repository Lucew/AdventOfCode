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


def main1(k=1):

    # get the field
    field = [list(line) for line in read_input()]

    # check for empty rows
    empty_rows = sorted(idx for idx, row in enumerate(field) if all(ele == "." for ele in row))
    empty_cols = sorted([cx for cx in range(len(field[0])) if all(row[cx] == "." for row in field)])

    # go through each line and find all the galaxies and calculate distance to partners
    galaxies = []
    result = 0
    cnt = 0
    for rx, row in enumerate(field):
        for cx, ele in enumerate(row):

            # check if ele is void (we could continue then)
            if ele == ".":
                continue

            # we found a galaxy and now compute the steps between the galaxies with under consideration of the
            # dilation of the universe (finding empty rows and cols between)
            cnt += 1
            for orx, ocx, ocnt in galaxies:

                # get minimum and maximum row
                minrx, maxrx = sorted((rx, orx))
                mincx, maxcx = sorted((cx, ocx))

                # find the number of dilated rows and cols in the way
                num_rows = bisect_left(empty_rows, maxrx) - bisect(empty_rows, minrx)
                num_rows = max(0, num_rows)
                num_cols = bisect_left(empty_cols, maxcx) - bisect(empty_cols, mincx)
                num_cols = max(0, num_cols)

                # compute the distance
                result += (maxrx-minrx) + (maxcx-mincx) + k*num_rows + k*num_cols

            # append the galaxy for other galaxies to be found
            galaxies.append((rx, cx, cnt))
    if k == 1:
        print(f'The result for solution 1 is: {result}')
    return result


def main2():
    print(f'The result for solution 2 is: {main1(k=1000000-1)}')


if __name__ == '__main__':
    main1()
    main2()
