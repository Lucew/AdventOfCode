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
    return inputs[0], inputs[1:]


def main1():

    # get the seeds and the lines
    seeds, lines = read_input()
    seeds = seeds[len("seeds: "):]
    seeds = [int(ele) for ele in seeds.split(" ")]

    # make the lines into the different subgroups
    translators = dict()
    last = ""
    counter = 0
    for line in lines:
        if line and not line[0].isnumeric():
            counter += 1
            last = f"{counter}_{line.split(' ')[0]}"
            translators[last] = []
        elif line:
            numbers = [int(ele) for ele in line.split(" ")]
            translators[last].append((numbers[1], numbers[1]+numbers[2]-1, numbers[0]-numbers[1]))

    # for each seed go through the steps
    steps = [(key, sorted(values)) for key, values in translators.items()]
    steps.sort()
    result = float("inf")
    for seed in seeds:
        # go through the steps
        for _, values in steps:

            # find the right interval
            idx = bisect(values, (seed, float("inf"), float("inf")))-1

            # check whether we are before or after or not in interval
            if idx < 0 or idx >= len(values) or values[idx][1] < seed:
                seed = seed
            else:
                seed = seed + values[idx][2]
        result = min(result, seed)

    print(f'The result for solution 1 is: {result}')


def main2():

    # get the seeds and the lines
    seeds, lines = read_input()
    seeds = seeds[len("seeds: "):]
    seeds = [[int(ele1), int(ele1)+int(ele2)-1] for ele1, ele2 in zip(seeds.split(" ")[:-1:2], seeds.split(" ")[1::2])]

    # make the lines into the different subgroups
    translators = dict()
    last = ""
    counter = 0
    for line in lines:
        if line and not line[0].isnumeric():
            counter += 1
            last = f"{counter}_{line.split(' ')[0]}"
            translators[last] = []
        elif line:
            numbers = [int(ele) for ele in line.split(" ")]
            translators[last].append((numbers[1], numbers[1] + numbers[2] - 1, numbers[0] - numbers[1]))

    # make the steps and the seeds and sort them how we need to do it
    steps = [(key, sorted(values)) for key, values in translators.items()]
    steps.sort()

    # make a stack with the seed ranges
    queue = [(0, ranges) for ranges in seeds]

    # go until the queue is empty
    result = float("inf")
    debug = False
    while queue:

        if debug:
            print(queue)
            print()
        # get the current steps and seedrange
        step, seedrange = queue.pop()

        # check whether we reached the last step
        if step >= len(steps):
            result = min(result, seedrange[0])
            continue

        # get the intervals for the steps
        intervals = steps[step][1]
        ends = [ele[1] for ele in intervals]

        # find the start interval
        sidx = bisect_left(ends, seedrange[0])

        # find the end interval
        eidx = bisect(ends, seedrange[1])
        if debug:
            print(seedrange, intervals, sidx, eidx)

        # check whether we start smaller than the first interval
        if sidx < 0:
            queue.append((step + 1, [seedrange[0], min(intervals[0][0] - 1, seedrange[1])]))
            sidx += 1
            seedrange[0] = intervals[0][0]

        # check whether we end after the last interval
        if eidx >= len(intervals):
            queue.append((step + 1, [max(seedrange[0], intervals[-1][1] + 1), seedrange[1]]))
            eidx -= 1
            seedrange[1] = intervals[-1][1]

        # go through the existing intervals
        for idx in range(sidx, eidx+1):

            # get the change parameters
            inc = intervals[idx][2]

            # check whether our current seed range starts before the current interval
            # which means there we some non mapping intervals in between
            if seedrange[0] < intervals[idx][0]:
                queue.append((step + 1, [seedrange[0], intervals[idx][0]-1]))

            # append the current seed range and changed seeds
            queue.append((step+1, [max(intervals[idx][0], seedrange[0])+inc, min(intervals[idx][1], seedrange[1])+inc]))

            # update the seed range
            seedrange[0] = intervals[idx][1]+1
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
