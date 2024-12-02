from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append([int(ele) for ele in line.split(' ')])
    return inputs


def check_report(report: list[int]):
    # compute the diff
    diffs = [ele1 - ele2 for ele1, ele2 in zip(report, report[1:])]

    # check the diffs
    rn_ele = next(iter(diffs))
    lost = [idx for idx, ele in enumerate(diffs) if (ele < 0) != (rn_ele < 0) or abs(ele) < 1 or abs(ele) > 3]
    return lost


def main1():
    result = 0

    # get the reports
    reports = read_input()

    # check for safety by calculating diffs and putting them into set
    for report in reports:
        # check whether they all have the same sign and they are between 1 and 3
        result += len(check_report(report)) == 0
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # get the reports
    reports = read_input()

    # check for safety by calculating diffs and putting them into set
    for report in reports:

        # check whether there are things wrong
        wrongs = check_report(report)
        if len(wrongs) == 0:
            result += 1
            continue

        # go through and check whether excluding one of two faulty levels helps
        vs = [ele for idx, ele in enumerate(report) if idx != wrongs[0]+1]
        if len(check_report(vs)) == 0:
            result += 1
            continue
        vs = [ele for idx, ele in enumerate(report) if idx != wrongs[0]]
        if len(check_report(vs)) == 0:
            result += 1
            continue

        # we also need to prune the first element in case that is the wrong one (as
        # we use it to check the sign)
        vs = report[1:]
        if len(check_report(vs)) == 0:
            result += 1
            continue

    print(f'The result for solution 1 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
