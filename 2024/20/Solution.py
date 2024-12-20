import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(list(line))
    return inputs


def draw_map(mapped: list[list[str]], path: list[tuple[(int, int)]] = None):

    # copy the map
    mapped = [row[:] for row in mapped]

    # check of path is not none and draw it in the map
    if path:
        for rx, cx in path:
            mapped[rx][cx] = 'o' if mapped[rx][cx] == '.' else mapped[rx][cx]

    # print the mapped
    for row in mapped:
        print(''.join(row))


def find_path(mapped: list[list[str]], start_rx, start_cx, target: str):

    # make dijkstra through the elements (we can use simple bfs, as all costs are equal)
    rx = start_rx
    cx = start_cx
    m = len(mapped)
    n = len(mapped[0])

    queue = collections.deque([(0, rx, cx)])
    visited = {(rx, cx): (-1, -1)}
    while queue:

        # get the current positions
        steps, rx, cx = queue.popleft()

        # go through the neighbors
        for nrx, ncx in [(rx + 1, cx), (rx - 1, cx), (rx, cx + 1), (rx, cx - 1)]:

            # check whether we are in bound and have not yet visited before
            if 0 <= nrx < m and 0 <= ncx < n and (nrx, ncx) not in visited and mapped[nrx][ncx] != '#':

                # save the path
                visited[nrx, ncx] = (rx, cx)

                # check whether we have reached the target
                if mapped[nrx][ncx] == target:

                    # recreate the path from the end
                    curr_pos = (nrx, ncx)
                    path = [(nrx, ncx)]
                    while curr_pos[0] >= 0:
                        curr_pos = visited[curr_pos]
                        if curr_pos[0] >= 0:
                            path.append(curr_pos)
                    return path[::-1]

                queue.append((steps + 1, nrx, ncx))
    return []


def main1():

    # get the map into the memory
    mapped = read_input()
    m = len(mapped)
    n = len(mapped[0])

    # find the start within the map
    start = (0, 0)
    end = (0, 0)
    for rx, row in enumerate(mapped):
        for cx, col in enumerate(row):
            if col == 'S':
                start = (rx, cx)
            elif col == 'E':
                end = (rx, cx)

    # find the path through the map
    path = find_path(mapped, start_rx=end[0], start_cx=end[1], target='S')
    maxlen = len(path)

    # save how many steps each path position has to the target
    steps_to_target = {pos: rx for rx, pos in enumerate(path)}

    # go along the path and check for walls we can skip to save time while keeping track of our starts
    cheat_paths = collections.defaultdict(list)
    rx = start[0]
    cx = start[1]
    visited = {(rx, cx)}
    while (rx, cx) != end:

        # go through walls from the current position and check whether we meet the path again
        for nrx, ncx, direct in [(rx+2, cx, (1, 0)), (rx-2, cx, (-1, 0)), (rx, cx+2, (0, 1)), (rx, cx-2, (0, -1))]:
            if (nrx, ncx) not in visited and (nrx, ncx) in steps_to_target:
                new_path_len = maxlen-steps_to_target[(nrx, ncx)]-len(visited)-1
                cheat_paths[new_path_len].append((nrx-direct[0], ncx-direct[1]))

        # take the next step
        for nrx, ncx in [(rx + 1, cx), (rx - 1, cx), (rx, cx + 1), (rx, cx - 1)]:

            # check whether we are in bound and have not yet visited before
            if 0 <= nrx < m and 0 <= ncx < n and (nrx, ncx) not in visited and mapped[nrx][ncx] != '#':
                rx = nrx
                cx = ncx
                visited.add((nrx, ncx))

    # get the valid paths that save enough time
    valid_paths = {key: len(ls) for key, ls in sorted(cheat_paths.items()) if key >= 100}
    print(f'The result for solution 1 is: {sum(valid_paths.values())}')


def cheat_bfs(mapped, start_rx, start_cx, steps_to_target, cheat_steps):
    # go through walls from the current until we can not check anymore and get the positions, we come out at
    # lets do that using dfs, where the stopping conditions are:
    #
    # 1) The first step of the cheat is not into a wall
    # 2) We run out of cheats (steps, that we took)
    # 3) We have visited this tile while cheating
    # 4) We are out of the map
    #
    #
    # We need to check how much time we have saved, when:
    #
    # 4) We come out somewhere on the path to the target

    # get the map dimensions
    m = len(mapped)
    n = len(mapped[0])

    # make the stack for the dfs and keep track o
    positions = collections.deque([(0, start_rx, start_cx)])
    visited = {(start_rx, start_cx)}
    cheat_paths = dict()
    while positions:

        # get the current positions
        steps, rx, cx = positions.popleft()

        # check whether we ran out of cheats
        if steps == cheat_steps:
            continue

        # go through the neighbors
        for nrx, ncx in [(rx + 1, cx), (rx - 1, cx), (rx, cx + 1), (rx, cx - 1)]:

            # check whether we are out of bounds
            if nrx < 0 or nrx >= m or ncx < 0 or ncx >= n:
                continue

            # check whether we have visited before
            if (nrx, ncx) in visited:
                continue

            # check whether we met the original path again
            if (nrx, ncx) in steps_to_target:
                new_path_len =  steps_to_target[(start_rx, start_cx)] - steps_to_target[(nrx, ncx)] - (steps + 1)
                cheat_paths[(start_rx, start_cx, nrx, ncx)] = new_path_len

            # otherwise append to the dfs
            visited.add((nrx, ncx))
            positions.append((steps+1, nrx, ncx))
    return cheat_paths


def main2(cheat_steps: int = 20, threshold: int = 100):

    # get the map into the memory
    mapped = read_input()

    # find the start within the map
    start = (0, 0)
    end = (0, 0)
    for rx, row in enumerate(mapped):
        for cx, col in enumerate(row):
            if col == 'S':
                start = (rx, cx)
            elif col == 'E':
                end = (rx, cx)

    # find the path through the map
    path = find_path(mapped, start_rx=end[0], start_cx=end[1], target='S')

    # save how many steps each path position has to the target
    steps_to_target = {pos: rx for rx, pos in enumerate(path)}

    # go along the path and check for walls we can skip to save time while keeping track of our starts
    cheat_paths = dict()
    for (rx, cx) in steps_to_target:

        # get the cheat paths from this position
        curr_cheat_paths = cheat_bfs(mapped, rx, cx, steps_to_target, cheat_steps)
        for key, val in curr_cheat_paths.items():
            cheat_paths[key] = max(cheat_paths.get(key, -float('inf')), val)

    # get the valid paths that save enough time
    occurence_counter = collections.Counter(val for val in cheat_paths.values() if val >= threshold)
    # print(sorted(occurence_counter.items()))
    print(f'The result for solution 2 is: {sum(val >= threshold for val in cheat_paths.values())}')


if __name__ == '__main__':
    main1()
    main2()
