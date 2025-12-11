import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    inputs = dict()
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            start, targets = line.split(': ')
            inputs[start] = targets.split(' ')
    return inputs


def main1():

    # get the inputs
    graph = read_input()

    # go through the graph via backtracking
    if not "you" in graph:
        print('Wrong input example. You not a starting position in graph.')
        return
    @functools.lru_cache(maxsize=None)
    def backtrack(pos: str):
        if pos == 'out':
            return 1
        return sum(backtrack(target) for target in graph[pos])
    result = backtrack('you')
    print(f'The result for solution 1 is: {result}')


def main2():

    # get the inputs
    graph = read_input()

    # go through the graph via backtracking
    @functools.lru_cache(maxsize=None)
    def backtrack(pos: str, visited: tuple[int, int]):
        if pos == 'out':
            return sum(visited) == 2
        # check whether we visited dac or fft
        if pos == 'dac':
            visited = (1, visited[1])
        if pos == 'fft':
            visited = (visited[0], 1)
        return sum(backtrack(target, visited) for target in graph[pos])

    result = backtrack('svr', (0, 0))
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
