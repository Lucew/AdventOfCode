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


def all_path_dijkstra(mapped, start, target, debug: bool = False):

    # get the dimension of the map
    m = len(mapped)
    n = len(mapped[0])
    if debug:
        print('Path:', start, target)

    # get the start position
    rx, cx = 0, 0
    for nrx, row in enumerate(mapped):
        for ncx, ch in enumerate(row):
            if ch == start:
                rx = nrx
                cx = ncx

    if debug:
        print('Start:', rx, cx)
    # get the shortest path using dijkstra (bfs as edge weights are equal)
    queue = collections.deque([(0, rx, cx, tuple())])
    visited = {(rx, cx): 0}
    shortest_paths = []
    while queue:

        # get the current positions
        steps, rx, cx, path = queue.popleft()

        # check that we reached the correct symbol
        if mapped[rx][cx] == target:
            shortest_paths.append((*path, 'A'))
            visited[(rx, cx)] = steps + 1
            continue

        # go to the neighbors
        for nrx, ncx, direct in [(rx + 1, cx, 'v'), (rx - 1, cx, '^'), (rx, cx + 1, '>'), (rx, cx - 1, '<')]:
            if 0 <= nrx < m and 0 <= ncx < n and mapped[nrx][ncx] != '.':

                # check whether we have taken longer than a path before
                if steps + 1 > visited.get((nrx, ncx), float('inf')):
                    continue

                # make the new path
                new_path = (*path, direct)

                # go further
                queue.append((steps + 1, nrx, ncx, new_path))
                visited[(nrx, ncx)] = steps + 1
    if debug:
        print(shortest_paths)
        print()
    return shortest_paths


@functools.cache
def traverse_keypad(start: str, target: str):

    # create the keypad
    keypad = ["789", "456", "123", ".0A"]
    return all_path_dijkstra(keypad, start, target)


@functools.cache
def traverse_dirpad(start: str, target: str):

    # create the map
    dirpad = [".^A", "<v>"]

    return all_path_dijkstra(dirpad, start, target)

@functools.cache
def go_path(word: tuple[str], level: int = 2, start_level: int = 2):

    # make this recursive with cache! this is possible as they will always come back to the 'A' button!
    word = ('A', *word)
    cost = 0
    for pdx, ch in enumerate(word[1:]):

        # get the new segment
        if level == start_level:
            seg = traverse_keypad(word[pdx], ch)
        else:
            seg = traverse_dirpad(word[pdx], ch)

        # traverse deeper with the segment
        if level == 0:
            cost += min(len(ps) for ps in seg)
        else:
            cost += min(go_path(ps, level-1, start_level) for ps in seg)
    return cost

def main1():
    result = 0

    # get the input from the file
    words = read_input()

    # go through the words
    for word in words:
        result += go_path(tuple(word)) * int(word.replace("A", ""))
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # get the input from the file
    words = read_input()

    # go through the words
    for word in words:
        result += go_path(tuple(word), 25, 25) * int(word.replace("A", ""))
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
