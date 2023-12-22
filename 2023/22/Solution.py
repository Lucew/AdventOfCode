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

            # separate the beginning and end
            coords = line.split("~")

            # get the coordinates into ints
            currblock = [[int(ele) for ele in block.split(",")] for block in coords]
            currblock = sorted(currblock, key=lambda x: x[2])
            inputs.append(currblock)

    # sort the inputs after the last coordinate so the lowest comes first
    inputs.sort(key=lambda x: x[0][2])
    return inputs


def main1(blocks: list[[(int, int, int), (int, int, int)]] = None):

    # get the inputs as blocks
    for_two = True
    if blocks is None:
        for_two = False
        blocks = read_input()

    # get the ground span
    max_x = 0
    max_y = 0
    for b1, b2 in blocks:
        assert all(ele >= 0 for ele in b1) and all(ele >= 0 for ele in b2), "Negative coordinates!"
        max_x = max(max_x, b1[0], b2[0])
        max_y = max(max_y, b1[1], b2[1])

    # span the ground
    ground = [[(1, -1) for _ in range(max_x+1)] for _ in range(max_y+1)]

    # save which blocks lie on others
    supported_by = [set() for _ in range(len(blocks))]

    # keep track of which blocks rest on which
    supports = [set() for _ in range(len(blocks))]

    # go through the blocks and update the ground
    for bx, ((x1, y1, z1), (x2, y2, z2)) in enumerate(blocks):

        # sort the coordinates
        y1, y2 = sorted((y1, y2))
        x1, x2 = sorted((x1, x2))

        # check the in the span for maximum height and blocks we are touching
        max_height = 0
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):

                # if new max height update the max height and clear the touches
                if ground[y][x][0] > max_height:
                    supported_by[bx].clear()
                    max_height = ground[y][x][0]

                # check whether we touch a new block
                if ground[y][x][0] == max_height and ground[y][x][1] >= 0:
                    supported_by[bx].add(ground[y][x][1])

        # go over the blocks we rest upon and make them aware that we lie on them
        for supporter in supported_by[bx]:
            supports[supporter].add(bx)

        # go over and update the max height
        height = z2-z1+1
        assert height > 0, "Something is off."
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                ground[y][x] = (max_height+height, bx)

        # update the block coordinate (to process part two)
        blocks[bx][0][2] = max_height
        blocks[bx][1][2] = max_height+height-1

    # make a set of blocks
    if not for_two:
        possible_blocks = set(range(len(blocks)))
        for tx, touch in enumerate(supported_by):
            if len(touch) == 1:
                possible_blocks.discard(touch.pop())
        print(f'The result for solution 1 is: {len(possible_blocks)}')
    return blocks, supports, supported_by


def main2():
    result = 0

    # get the screenshot of the blocks
    blocks = read_input()

    # let the blocks fall and rest
    blocks, supports, supported_by = main1(blocks)

    # make bfs from below for each block until no blocks falls anymore
    # and keep track of the visited
    for bx in range(len(blocks)):

        # put this block into a queue to make bfs as long as the next block falls
        stack = collections.deque([bx])
        curr_falling = {bx}
        while stack:

            # get the current block
            curr_bx = stack.popleft()

            # get the stones we are supporting and check whether each of them falls (is only supported by blocks
            # that have been fallen already)
            for supported_by_current in supports[curr_bx]:
                if len(supported_by[supported_by_current] - curr_falling) == 0:
                    curr_falling.add(supported_by_current)
                    stack.append(supported_by_current)

        # check how many blocks have fallen
        result += len(curr_falling)-1
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
