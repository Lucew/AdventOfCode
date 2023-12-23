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


SLOPES = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}


def pretty_print(lines, path):
    for rx, row in enumerate(lines):
        tmp = []
        for cx, ele in enumerate(row):
            if (rx, cx) in path:
                tmp.append("O")
            else:
                tmp.append(ele)
        print("".join(tmp))


def main1():

    # get the input
    lines = read_input()

    # make a queue that contains the paths itself and give them an ID
    stop_it = set()
    queue = collections.deque([(0, 0, 1, {(0, 1)})])
    next_id = 1
    visited = collections.defaultdict(dict)
    visited[(0, 1)][0] = 0
    while queue:

        # get the current position and ID
        curr_id, rx, cx, path = queue.popleft()

        # check whether we have been deleted
        if curr_id in stop_it:
            stop_it.remove(curr_id)
            continue

        # go through the neighbors
        for nrx, ncx, allowed in [(rx+1, cx, "v"), (rx-1, cx, "^"), (rx, cx+1, ">"), (rx, cx-1, "<")]:

            # check if we are out of bounds or have visited this tile before
            if nrx < 0 or ncx < 0 or nrx >= len(lines) or ncx >= len(lines[0]):
                continue

            # check whether there is forest or a not allowed slope
            if lines[nrx][ncx] == "#" or (lines[nrx][ncx] != "." and lines[nrx][ncx] != allowed):
                continue

            # make a copy of the path
            cop_path = {ele for ele in path}
            cop_path.add((nrx, ncx))

            # make the slope update
            drx, dcx = SLOPES.get(lines[nrx][ncx], (0, 0))
            nrx += drx
            ncx += dcx

            # check whether we have visited before
            if (nrx, ncx) in path:
                continue

            # calculate our new path length
            path_length = len(cop_path)+abs(drx+dcx)

            # add all paths that have visited with less length to the delete information
            keys = list(visited[(nrx, ncx)].keys())
            currdict = visited[(nrx, ncx)]
            delete = False
            for key in keys:
                if currdict[key] >= path_length:
                    delete = True
                if currdict[key] < path_length:
                    stop_it.add(key)
                    del currdict[key]

            # check whether we have been deleted
            if delete:
                continue

            # add us to the paths that have been there and to the queue (and update the ids)
            currdict[next_id] = path_length

            if nrx == len(lines) - 1 and ncx == len(lines[0]) - 2:
                pass
            queue.append((next_id, nrx, ncx, cop_path | {(nrx, ncx)}))
            next_id += 1
    print(f'The result for solution 1 is: {max(visited[(len(lines)-1, len(lines[0])-2)].values())-1}')


def main2():

    # get the input
    lines = read_input()

    # get the junctions as nodes, so we traverse a little faster
    junctions = collections.defaultdict(list)
    for rx, row in enumerate(lines):
        for cx, ele in enumerate(row):

            # forest can not be a junction
            if ele == '#':
                continue

            # check the surrounding
            for nrx, ncx in [(rx + 1, cx), (rx - 1, cx), (rx, cx + 1), (rx, cx - 1)]:
                # check if we are out of bounds or have visited this tile before
                if nrx < 0 or ncx < 0 or nrx >= len(lines) or ncx >= len(lines[0]):
                    continue

                # check whether there is forest or a not allowed slope
                if lines[nrx][ncx] == "#":
                    continue

                # add the continuation to the junctions
                junctions[(rx, cx)].append((nrx, ncx))

            # only keep the junctions that have more than two directions
            if len(junctions[(rx, cx)]) <= 2 and (rx, cx) != (0, 1) and (rx, cx) != (len(lines)-1, len(lines[0])-2):
                del junctions[(rx, cx)]

    # go from every junction until we find another one to get the longest path
    # between junctions
    junction_dist = collections.defaultdict(dict)
    junction_list = list(junctions.keys())
    for junc in junction_list:

        # get the indices from it
        rx, cx = junc

        # make a queue to do bfs
        queue = collections.deque([(nrx, ncx, 1) for nrx, ncx in junctions[junc]])
        visited = {(rx, cx)}
        while queue:

            # get current position and steps
            rx, cx, steps = queue.popleft()

            # go to the neighbors
            for nrx, ncx in [(rx + 1, cx), (rx - 1, cx), (rx, cx + 1), (rx, cx - 1)]:

                # check if we are out of bounds or have visited this tile before
                if nrx < 0 or ncx < 0 or nrx >= len(lines) or ncx >= len(lines[0]):
                    continue

                # check whether there is forest or a not allowed slope
                if lines[nrx][ncx] == "#":
                    continue

                # check whether we have been there
                if (nrx, ncx) in visited:
                    continue

                # check whether we have reached another junction
                if (nrx, ncx) in junctions:
                    junction_dist[junc][(nrx, ncx)] = steps+1
                    junction_dist[(nrx, ncx)][junc] = steps+1
                    continue

                # append to the queue
                visited.add((nrx, ncx))
                queue.append((nrx, ncx, steps+1))

    # make a queue that contains the paths itself and give them an ID
    result = 0
    queue = collections.deque([(0, 1, 0, {(0, 1)})])
    while queue:

        # get the current position and ID
        rx, cx, dist, path = queue.popleft()

        # go through the neighbors
        for njunc, ndist in junction_dist[(rx, cx)].items():

            # check whether we have visited before
            if njunc in path:
                continue

            # check whether we reached the end
            if njunc[0] == len(lines) - 1 and njunc[1] == len(lines[0]) - 2:
                result = max(result, dist+ndist)
                continue

            # add us to the paths that have been there and to the queue (and update the ids)
            queue.append((njunc[0], njunc[1], dist+ndist, path | {njunc}))
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
