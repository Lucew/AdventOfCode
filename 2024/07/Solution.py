from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            # get the result and the test numbers
            result, test_numbers = line.split(': ')
            test_numbers = [int(ele) for ele in test_numbers.split(' ')]
            inputs.append((int(result), test_numbers))
    return inputs


def eq_check_valid(numbers: list[int], target: int, concatenation: bool = False):

    # create a stack for possible solutions (dfs but without recursion)
    stack = [(numbers[0], 0)]
    n = len(numbers)-1
    while stack:

        # get the current position
        val, nx = stack.pop()

        # check whether we can not reach the target anymore
        if val > target:
            continue

        # make the new pointer
        nx += 1

        # make addition of next number
        updated_number_add = val + numbers[nx]
        if nx == n:
            if updated_number_add == target:
                return True
        else:
            stack.append((updated_number_add, nx))

        # make multiplication
        updated_number_mult = val * numbers[nx]
        if nx == n:
            if updated_number_mult == target:
                return True
        else:
            stack.append((updated_number_mult, nx))

        # check whether concatenation is possible
        if not concatenation:
            continue

        # make the concatenation
        updated_number_concat = val*10**(len(str(numbers[nx]))) + numbers[nx]
        if nx == n:
            if updated_number_concat == target:
                return True
        else:
            stack.append((updated_number_concat, nx))
    return False


def main1():

    # get the input
    eqs = read_input()

    # go through the inputs and try to check whether a solution is valid
    result = sum(target for target, numbers in eqs if eq_check_valid(numbers, target))

    print(f'The result for solution 1 is: {result}')


def main2():

    # get the input
    eqs = read_input()

    # go through the inputs and try to check whether a solution is valid
    result = sum(target for target, numbers in eqs if eq_check_valid(numbers, target, concatenation=True))
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
