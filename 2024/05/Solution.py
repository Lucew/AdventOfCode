import collections
import itertools
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect
import re


def read_input(path: str = 'input.txt'):
    order = []
    updates = []
    sv = order
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()

            # check whether we need to switch the saving variable
            if not line:
                sv = updates
            else:
                sv.append([int(ele) for ele in re.split('[|,]', line)])
    return order, updates


def main1():
    result = 0

    # get the input
    order, updates = read_input()

    # create the graph with all elements that come before it
    graph = collections.defaultdict(set)
    for before, after in order:
        graph[before].add(after)

    # go through the updates and check whether we find a page at some position which has pages
    # before it that it is a precondition for
    invalid = []
    for update in updates:
        printed = set()
        valid = True
        for page in update:
            if printed & graph[page]:
                valid = False
                break
            else:
                printed.add(page)
        if valid:
            result += update[len(update)//2]
        else:
            invalid.append(update)
    print(f'The result for solution 1 is: {result}')
    return invalid


def topological_sort(graph):

    # create a counter how many incoming edges every node has
    cn = {ele: 0 for ele in graph}
    for origin, targets in graph.items():
        for target in targets:
            cn[target] += 1

    # get all the root elements
    roots = [ele for ele, cns in cn.items() if cns == 0]
    ordered_list = []
    while roots:

        # get the current root
        root = roots.pop()

        # append it to the sorted list
        ordered_list.append(root)

        # go through and reduce the edge counter
        for target in graph[root]:
            cn[target] -= 1
            if cn[target] == 0:
                roots.append(target)
    return ordered_list



def main2():
    result = 0

    # get the input
    order, updates = read_input()

    # create the graph with all elements that come before it
    graph = set(ele for listed in itertools.chain(order, updates) for ele in listed)
    graph = {ele: set() for ele in graph}
    for before, after in order:
        graph[before].add(after)

    # get the invalid things
    invalid = main1()

    # go through the updates and do a topological sort
    for update in invalid:

        # get the subgraph that is interesting for us
        elements = set(update)
        subgraph = {ele: elements&graph[ele] for ele in elements}

        # make the topological sort
        update = topological_sort(subgraph)

        # update the result
        result += update[len(update) // 2]

    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main2()
