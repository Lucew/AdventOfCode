import collections
from collections import Counter, defaultdict, OrderedDict
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


class SparsePlatform:

    def __init__(self, platform: list[str]):

        # save some parameters
        self._shape = (len(platform), len(platform[0]))
        self._rotation = 0

        # create the internal representation
        self._elements = {(rx, cx): ele for rx, row in enumerate(platform) for cx, ele in enumerate(row) if ele != "."}

    def rotate_platform(self, degree: int = 90):

        # check the rotation parameter
        assert degree % 90 == 0, f"Rotation needs to be multiple of 90°. You gave: {degree}."
        self._rotation = (self._rotation + degree) % 360
        return self

    def reset(self):
        self._rotation = 0
        return self

    def shape(self):
        # get check whether we need to swap the axis
        return list(reversed(self._shape)) if self._rotation % 180 == 90 else list(self._shape)

    def _convert_idx(self, rx, cx):
        # get the original shape
        m, n = self._shape

        # make the conversion
        if self._rotation == 0:
            nrx = rx
            ncx = cx
        elif self._rotation == 90:
            nrx = n - cx - 1
            ncx = rx
        elif self._rotation == 180:
            nrx = n-rx-1
            ncx = m-cx-1
        elif self._rotation == 270:
            nrx = cx
            ncx = m - rx - 1
        else:
            raise ValueError(f"Rotation is illegal: {self._rotation}.")
        return nrx, ncx

    def __getitem__(self, key: (int, int)):
        rx, cx = self._convert_idx(*key)
        return self._elements.get((rx, cx), ".")

    def __setitem__(self, key: (int, int), value: str):
        rx, cx = self._convert_idx(*key)
        self._elements[(rx, cx)] = value

    def delete(self, key):
        rx, cx = self._convert_idx(*key)
        del self._elements[(rx, cx)]

    def __repr__(self):
        m, n = self.shape()
        return "\n".join("".join(self[rx, cx] for cx in range(n)) for rx in range(m))

    def __hash__(self):
        return hash(frozenset(pos for pos, ele in self._elements.items() if ele == 'O'))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return all(other._elements[key] == value for key, value in self._elements)

    def copy(self):
        return self.__class__(str(self).split("\n"))

    def tilt(self):

        # get the shape
        m, n = self.shape()

        stopped = [0] * n
        for cx in range(n):
            for rx in range(m):

                # get the element
                ele = self[(rx, cx)]

                # check if we find a square rock
                if ele == "#":
                    stopped[cx] = rx + 1

                # check if we find a rolling rock
                elif ele == "O":

                    # delete the old element
                    self.delete((rx, cx))

                    # set the new element
                    self[(stopped[cx], cx)] = ele

                    # update the stop
                    stopped[cx] += 1

    def cycle(self):
        for _ in range(4):
            self.tilt()
            self.rotate_platform()
        return self

    def north_load(self):
        m, n = self.shape()
        load = 0
        for rx in range(m):
            for cx in range(n):
                if self[rx, cx] == "O":
                    load += m-rx
        return load


def main1():
    result = 0
    lines = read_input()
    stopped = [0]*len(lines[0])
    for rx, line in enumerate(lines):
        for cx, ele in enumerate(line):

            # check if we find a square rock
            if ele == "#":
                stopped[cx] = rx+1
            # check if we find a rollin rock
            elif ele == "O":

                # roll the rock, add the weight and add the stop point
                result += len(lines)-stopped[cx]
                stopped[cx] += 1
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # make the sparse platform
    sparse = SparsePlatform(read_input())

    # cycle the platform until it reaches a visited status
    visited = dict()
    cnt = 0
    while hash(sparse) not in visited:
        visited[hash(sparse)] = cnt
        cnt += 1
        sparse = sparse.cycle()

    # find the cycle length
    cycle_length = cnt-visited[hash(sparse)]
    cycle_start = visited[hash(sparse)]

    # create a new representation and cycle it
    sparse = SparsePlatform(read_input())
    for _ in range(cycle_start+(1000000000-cycle_start) % cycle_length):
        sparse.cycle()
    print(f'The result for solution 2 is: {sparse.north_load()}')


if __name__ == '__main__':
    main1()
    main2()
