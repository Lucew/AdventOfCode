import collections
import heapq
import functools
import bisect
import math


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(tuple(int(ele) for ele in line.split(',')))
    return inputs


def find_set(element: int, parents: list[int]) -> int:
    if element == parents[element]:
        return element
    parents[element] = find_set(parents[element], parents)
    return parents[element]


def union(element1: int, element2: int, parents: list[int], sizes: list[int]) -> int:
    element1 = find_set(element1, parents)
    element2 = find_set(element2, parents)
    if element1 != element2:

        # check who has the larger tree
        if sizes[element1] < sizes[element2]:
            parents[element1] = element2
            sizes[element2] += sizes[element1]
            size = sizes[element2]
        else:
            parents[element2] = element1
            sizes[element1] += sizes[element2]
            size = sizes[element1]
    return max(sizes[element1], sizes[element2])


def main1():

    # get the coordinates
    inputs = read_input()

    # make the groups for each of the boxes
    parents = list(range(len(inputs)))
    sizes = [1]*len(inputs)

    # compute the pairwise distances
    distances = []
    for idx1, (x1,y1,z1) in enumerate(inputs):
        for idx2, (x2,y2,z2) in enumerate(inputs[idx1+1:], idx1+1):
            distances.append((((x1-x2)**2+(y1-y2)**2+(z1-z2)**2), (idx1, idx2)))

    # transform distances into a heap
    heapq.heapify(distances)

    # pop from the heap
    for _ in range(1000):

        # get the distance
        d1, (idx1, idx2) = heapq.heappop(distances)

        # union the sets
        union(idx1, idx2, parents, sizes)

    # find the three largest groups by the sizes
    result = functools.reduce(lambda x,y: x*y, heapq.nlargest(3, sizes), 1)

    print(f'The result for solution 1 is: {result}')


def main2():

    # get the coordinates
    inputs = read_input()

    # make the groups for each of the boxes
    parents = list(range(len(inputs)))
    sizes = [1] * len(inputs)

    # compute the pairwise distances
    distances = []
    for idx1, (x1, y1, z1) in enumerate(inputs):
        for idx2, (x2, y2, z2) in enumerate(inputs[idx1 + 1:], idx1 + 1):
            distances.append((((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2), (idx1, idx2)))

    # transform distances into a heap
    heapq.heapify(distances)

    # pop from the heap
    for _ in range(len(inputs)*len(inputs)//2):
        # get the distance
        d1, (idx1, idx2) = heapq.heappop(distances)

        # union the sets
        cursize = union(idx1, idx2, parents, sizes)
        if cursize == len(inputs):
            cable_length = inputs[idx1][0] * inputs[idx2][0]
            print(f'The result for solution 2 is: {cable_length}')
            return 0
    raise NotImplementedError('Something went wrong with solution 2.')


if __name__ == '__main__':
    main1()
    main2()
