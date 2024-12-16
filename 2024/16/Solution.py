import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def main1():
    result = 0

    # get the map from the input
    mapped = read_input()

    # find the starting position
    position = [0, 0]
    goal = [0, 0]
    direction = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for rx, row in enumerate(mapped):
        for cx, ele in enumerate(row):
            if ele == 'S':
                position = [rx, cx]
            elif ele == 'E':
                goal = [rx, cx]

    # make dijkstra through the maze
    heap = [(0, position[0], position[1], direction)]
    visited = {(position[0], position[1])}
    new_costs = [1, 1001, 2001, 1001]
    while heap:

        # get the current position
        cost, rx, cx, direction = heapq.heappop(heap)

        # check for the neighbors in all directions
        for ndir in range(direction, direction+4):

            # get the cost for the new direction
            # by how we turn
            ncost = new_costs[(ndir-direction)]

            # get the new direction
            ndir = ndir % 4

            # update the current position
            nrx, ncx = rx+directions[ndir][0], cx+directions[ndir][1]

            # check whether we already visited this location
            if (nrx, ncx) in visited:
                continue

            # check whether we reached the goal
            if nrx == goal[0] and ncx == goal[1]:
                print(f'The result for solution 1 is: {cost + ncost}')
                return cost + ncost

            # check whether we reached a wall
            if mapped[nrx][ncx] == '#':
                continue

            # add the step to the heap
            heapq.heappush(heap, (cost + ncost, nrx, ncx, ndir))
            visited.add((nrx, ncx))

    print(f'Did not find a solution.')


def main2(maximum_costs: int):

    # get the map from the input
    mapped = read_input()

    # find the starting position
    position = [0, 0]
    goal = [0, 0]
    direction = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for rx, row in enumerate(mapped):
        for cx, ele in enumerate(row):
            if ele == 'S':
                position = [rx, cx]
            elif ele == 'E':
                goal = [rx, cx]

    # make dijkstra through the maze
    heap = [(0, position[0], position[1], direction, [(position[0], position[1])])]
    new_costs = [1, 1001, 2001, 1001]
    visited = {(position[0], position[1], direction): 0}
    valid_elements = set()
    while heap:

        # get the current position
        cost, rx, cx, direction, path = heapq.heappop(heap)

        # check for the neighbors in all directions
        for ndir in range(direction, direction + 4):

            # get the cost for the new direction
            # by how we turn
            ncost = new_costs[(ndir - direction)]

            # get the new direction
            ndir = ndir % 4

            # update the current position
            nrx, ncx = rx + directions[ndir][0], cx + directions[ndir][1]

            # check whether we reached the goal
            if nrx == goal[0] and ncx == goal[1]:
                valid_elements.update(path)
                valid_elements.add((nrx, ncx))
                continue

            # check whether we reached a wall
            if mapped[nrx][ncx] == '#':
                continue

            # check whether we were already there with lower costs
            if visited.get((nrx, ncx, ndir), float('inf')) < cost + ncost or cost+ncost >= maximum_costs:
                continue

            # add the step to the heap
            heapq.heappush(heap, (cost + ncost, nrx, ncx, ndir, path[:]+[(nrx, ncx)]))
            visited[(nrx, ncx, ndir)] = cost + ncost

    print(f'The result for solution 2 is: {len(valid_elements)}')


if __name__ == '__main__':
    main2(main1())
