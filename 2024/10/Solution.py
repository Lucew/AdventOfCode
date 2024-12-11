import collections
import functools


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append([-5 if ele == '.' else int(ele) for ele in line])
    return inputs


def main1():
    result = 0

    # get the input into memory
    mapped = read_input()
    m = len(mapped)
    n = len(mapped[0])

    # go from the nines and keep track, which tiles are reachable
    for __rx, row in enumerate(mapped):
        for __cx, val in enumerate(row):

            # check whether we encountered a starting position
            if val != 0: continue

            # set up a bfs and keep track of visited paths
            found_nines = 0
            queue = collections.deque([(__rx, __cx)])
            visited = {(__rx, __cx)}
            while queue:

                # get current position
                rx, cx = queue.popleft()

                # go to all four directions
                for nrx, ncx in [(rx+1, cx), (rx-1, cx), (rx, cx+1), (rx, cx-1)]:
                    if 0 <= nrx < m and 0 <= ncx < n and (nrx, ncx) not in visited and mapped[nrx][ncx] == mapped[rx][cx]+1:
                        visited.add((nrx, ncx))
                        if mapped[nrx][ncx] == 9:
                            found_nines += 1
                        else:
                            queue.append((nrx, ncx))
            # start at the current position
            result += found_nines
    print(f'The result for solution 1 is: {result}')

def main2():

    # get the input into memory
    mapped = read_input()
    m = len(mapped)
    n = len(mapped[0])

    # make a memoized dfs (and keep memory over the loop)
    @functools.cache
    def dfs(rx, cx):
        if mapped[rx][cx] == 9:
            return 1

        # go through all possible paths
        found_nines = 0
        for nrx, ncx in [(rx+1, cx), (rx-1, cx), (rx, cx+1), (rx, cx-1)]:
            if 0 <= nrx < m and 0 <= ncx < n and (nrx, ncx) and mapped[nrx][ncx] == mapped[rx][cx] + 1:
                found_nines += dfs(nrx, ncx)
        return found_nines

    # go from the nines and keep track, which tiles are reachable
    result = sum(dfs(__rx, __cx) for __rx, row in enumerate(mapped) for __cx, val in enumerate(row)
                 if mapped[__rx][__cx] == 0)

    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
