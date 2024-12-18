import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(tuple(map(int, line.split(',')[::-1])))
    return inputs


def pretty_print_bytes(falling_bytes: set[tuple[int, int]], m, n):
    field = [['.']*n for _ in range(m)]
    for rx, cx in falling_bytes:
        field[rx][cx] = '#'
    for line in field:
        print(''.join(line))


def main1(debug: bool = False):

    # define the available space
    if debug:
        max_rx = 7
        max_cx = 7
        end_dx = 12
    else:
        max_rx = 71
        max_cx = 71
        end_dx = 1024

    # get the input
    falling_bytes = set(read_input()[:end_dx])
    # pretty_print_bytes(falling_bytes, max_rx, max_cx)

    # make dijkstra through the elements (we can use simple bfs, as all costs are equal)
    queue = collections.deque([(0, 0, 0)])
    visited = {(0, 0)}
    while queue:

        # get the current positions
        steps, rx, cx = queue.popleft()

        # go through the neighbors
        for nrx, ncx in [(rx+1, cx), (rx-1, cx), (rx, cx+1), (rx, cx-1)]:

            # check whether this field is corrupted
            if (nrx, ncx) in falling_bytes:
                continue

            # check whether we are in bound and have not yet visited before
            if 0 <= nrx < max_rx and 0 <= ncx < max_cx and (nrx, ncx) not in visited:

                # check whether we have reached the target
                if nrx == max_rx-1 and ncx == max_cx-1:
                    return print(f'The result for solution 1 is: {steps+1}')

                queue.append((steps+1, nrx, ncx))
                visited.add((nrx, ncx))
    print('Something went wrong in solution 1.')


def find_path(falling_bytes: list[tuple[int, int]], max_rx: int, max_cx: int):

    # convert the falling bytes into a set for faster lookup
    falling_bytes = set(falling_bytes)

    # make dijkstra through the elements (we can use simple bfs, as all costs are equal)
    queue = collections.deque([(0, 0, 0)])
    visited = {(0, 0)}
    while queue:

        # get the current positions
        steps, rx, cx = queue.popleft()

        # go through the neighbors
        for nrx, ncx in [(rx + 1, cx), (rx - 1, cx), (rx, cx + 1), (rx, cx - 1)]:

            # check whether this field is corrupted
            if (nrx, ncx) in falling_bytes:
                continue

            # check whether we are in bound and have not yet visited before
            if 0 <= nrx < max_rx and 0 <= ncx < max_cx and (nrx, ncx) not in visited:

                # check whether we have reached the target
                if nrx == max_rx - 1 and ncx == max_cx - 1:
                    return True

                queue.append((steps + 1, nrx, ncx))
                visited.add((nrx, ncx))
    return False


def main2(debug: bool = False):

    # get the input
    falling_bytes = read_input()

    # define the available space
    if debug:
        max_rx = 7
        max_cx = 7
        end_dx = 12
    else:
        max_rx = 71
        max_cx = 71
        end_dx = 1024

    # do binary search on the input
    left = 0
    right = len(falling_bytes)+1
    result = 0
    while left < right:

        # check the middle
        mid = (left + right) // 2

        # check whether it works
        if find_path(falling_bytes[:mid], max_rx, max_cx):
            left = mid+1
            result = mid
        else:
            right = mid
    print(f'The result for solution 2 is: {",".join(str(ele) for ele in falling_bytes[result][::-1])}')


if __name__ == '__main__':
    main1()
    main2()
