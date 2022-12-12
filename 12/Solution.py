from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(list(line))
    return inputs


def main1(print_path=False):
    # get the inputs from the inputs
    inputs = read_input()

    # find the start
    start = None
    end = None
    for rx, row in enumerate(inputs):
        for cx, ele in enumerate(row):
            if ele == 'S':
                inputs[rx][cx] = 'a'
                start = (rx, cx)
            elif ele == 'E':
                inputs[rx][cx] = 'z'
                end = (rx, cx)
    assert start is not None, 'Did not find a start.'
    assert end is not None, 'Did not find end.'

    # make a matrix for the path costs to a node
    costs = [[float('inf')] * len(inputs[0]) for _ in range(len(inputs))]
    costs[start[0]][start[1]] = 0

    # make a dict to save the predecessors
    predecessors = dict()

    # make the path checking using dijkstra
    # for that we need a min heap
    heap = [(0, start[0], start[1])]
    seen = set()

    # go while the heap is existing
    while heap:

        # pop the current node
        cost, rx, cx = heappop(heap)

        # break if we found our target
        if (rx, cx) == end:
            print(f'The result for solution 1 is: {costs[rx][cx]}')
            break

        # check whether we have been cheaper
        if (rx, cx) in seen:
            continue

        # add node to seen
        seen.add((rx, cx))

        # go through the possible neighbours and check their costs
        for nrx, ncx in [(rx + 1, cx), (rx - 1, cx), (rx, cx + 1), (rx, cx - 1)]:
            # check the index for scope and whether the future costs are higher
            ncosts = cost + 1

            # the conditions to go to a neighbour are:
            #
            # 1) Row is in scope
            # 2) Column is in scope
            # 3) The character is reachable according to challenge conditions
            # 4) the costs are lower than any costs we have found before
            if 0 <= nrx < len(inputs) \
                    and 0 <= ncx < len(inputs[0]) \
                    and ord(inputs[rx][cx]) + 1 >= ord(inputs[nrx][ncx]) \
                    and costs[nrx][ncx] > ncosts:

                # put the current node as predecessor
                predecessors[(nrx, ncx)] = (rx, cx)

                # update the costs of the next node
                costs[nrx][ncx] = ncosts

                # add the next node to the queue
                heappush(heap, (ncosts, nrx, ncx))

    # reconstruct the path
    pred = []
    start = end

    # check if we want to end
    if not print_path:
        return

    while print_path and start in predecessors:
        pred.append(predecessors[start])
        start = predecessors[start]

    # reverse the path
    pred = pred[::-1]
    pred.append(end)

    # make a matrix
    pathes = [['.']*len(inputs[0]) for _ in range(len(inputs))]
    for idx, (rx, cx) in enumerate(pred[:-1], 1):
        nrx, ncx = pred[idx]
        if cx == ncx and rx < nrx:
            pathes[rx][cx] = 'v'
        elif cx == ncx and rx > nrx:
            pathes[rx][cx] = '^'
        elif rx == nrx and cx < ncx:
            pathes[rx][cx] = '>'
        elif rx == nrx and cx > ncx:
            pathes[rx][cx] = '<'

    # pretty print the path in a matrix
    for row in pathes:
        for ele in row:
            print(ele, end=' ')
        print()


def main2(print_path=False):

    # load the input
    inputs = read_input()

    # find the start
    start = None
    for rx, row in enumerate(inputs):
        for cx, ele in enumerate(row):
            if ele == 'E':
                start = (rx, cx)
                inputs[rx][cx] = 'z'
            if ele == 'S':
                inputs[rx][cx] = 'a'
    assert start is not None, 'Start was not found.'

    # make a heap and a predecessor dict for the path (initialize with the start point)
    heap = [(0, start[0], start[1])]
    predecessors = dict()
    seen = set()
    end = None

    # make an array for the costs
    costs = [[float('inf')]*len(inputs[0]) for _ in range(len(inputs))]
    costs[start[0]][start[1]] = 0

    # make the dijkstra while we have nodes in the heap
    while heap:

        # push a node with the lowest cost
        cost, rx, cx = heappop(heap)

        # check for the end condition
        if inputs[rx][cx] == 'a':
            end = (rx, cx)
            print(f'The result for solution 2 is: {costs[rx][cx]}')
            break

        # check whether we already finished this node
        if (rx, cx) in seen:
            continue

        # add node to seen
        seen.add((rx, cx))

        # add the next nodes to the queue
        for nrx, ncx in [(rx + 1, cx), (rx - 1, cx), (rx, cx + 1), (rx, cx - 1)]:
            # check the index for scope and whether the future costs are higher
            ncosts = cost + 1

            # the conditions to go to a neighbour are:
            #
            # 1) Row is in scope
            # 2) Column is in scope
            # 3) The character is reachable according to challenge conditions
            # 4) the costs are lower than any costs we have found before
            if 0 <= nrx < len(inputs) \
                    and 0 <= ncx < len(inputs[0]) \
                    and ord(inputs[rx][cx]) - 1 <= ord(inputs[nrx][ncx]) \
                    and costs[nrx][ncx] > ncosts:
                # put the current node as predecessor
                predecessors[(nrx, ncx)] = (rx, cx)

                # update the costs of the next node
                costs[nrx][ncx] = ncosts

                # add the next node to the queue
                heappush(heap, (ncosts, nrx, ncx))

    # make a sanity check
    assert end is not None, 'Did not find the target.'

    # reconstruct the path
    pred = []
    start = end

    # check if we want to end
    if not print_path:
        return

    while print_path and start in predecessors:
        pred.append(predecessors[start])
        start = predecessors[start]

    # reverse the path
    pred = pred[::-1]
    pred.append(end)

    # make a matrix
    pathes = [['.'] * len(inputs[0]) for _ in range(len(inputs))]
    for idx, (rx, cx) in enumerate(pred[:-1], 1):
        nrx, ncx = pred[idx]
        if cx == ncx and rx < nrx:
            pathes[rx][cx] = 'v'
        elif cx == ncx and rx > nrx:
            pathes[rx][cx] = '^'
        elif rx == nrx and cx < ncx:
            pathes[rx][cx] = '>'
        elif rx == nrx and cx > ncx:
            pathes[rx][cx] = '<'

    # pretty print the path in a matrix
    for row in pathes:
        for ele in row:
            print(ele, end=' ')
        print()


if __name__ == '__main__':
    main1()
    main2()
