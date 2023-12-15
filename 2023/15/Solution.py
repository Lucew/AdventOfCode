import collections
import functools
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


def update(curr_hash: int, curr: str):

    # get the current hash (anding with 255 is MOD256)
    curr_hash = (((curr_hash + ord(curr)) & 255)*17) & 255
    return curr_hash


def hashed(element: str):
    return functools.reduce(lambda before, curr: update(before, curr), element, 0)


def read_input(path: str = 'input.txt'):
    with open(path) as filet:
        line = filet.read()
    line = line.replace("\n", "")
    elements = [ele for ele in line.split(",")]
    return elements


def main1():
    result = 0

    # get the input parse
    elements = read_input()

    # go through the elements
    for element in elements:
        result += hashed(element)
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # get the input parse
    elements = read_input()
    boxes = collections.defaultdict(dict)

    # create the boxes
    for cnt, element in enumerate(elements):

        # check whether we need to remove a lens
        if element.endswith("-"):
            label = element[:-1]
            curr_hash = hashed(label)
            if label in boxes[curr_hash]:
                del boxes[curr_hash][label]
        else:
            label, focal_length = element.split("=")
            curr_hash = hashed(label)

            # save the position if lens was already there
            if label in boxes[curr_hash]:
                cnt, _ = boxes[curr_hash][label]

            # update the lens
            boxes[curr_hash][label] = [cnt, int(focal_length)]

    # go through the boxes and compute
    for box, lenses in boxes.items():
        lenses = sorted(lenses.values())
        box += 1
        for idx, (name, focal) in enumerate(lenses, 1):
            # print(box, idx, name, focal)
            result += box*idx*focal
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
