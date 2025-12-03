import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.extend(tuple(ele.split('-')) for ele in line.split(','))
    return inputs


def double_number(num: int) -> int:
    return num + num * 10**(len(str(num)))


def separate_numb(num: str) -> int:
    for sep in range(1, len(num)//2+1):
        if len(num) % sep == 0 and len(set(num[i*sep:(i+1)*sep] for i in range(len(num)//sep))) == 1:
            return int(num)
    return 0


def main1():
    result = 0
    inputs = read_input()

    for start, end in inputs:

        # get the number of digits of the start
        start_digs = len(start)

        # get the first starting number
        if start_digs == 1:
            starting_number = 1
        else:
            starting_number = int(start[:start_digs//2])

        # transform start and end
        start = int(start)
        end = int(end)

        # go through the numbers
        curnum = starting_number
        doublenum = double_number(curnum)
        while doublenum <= end:
            if start <= doublenum <= end:
                result += doublenum
            curnum += 1
            doublenum = double_number(curnum)
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0
    inputs = read_input()
    inputs = [tuple(int(ele) for ele in arr) for arr in inputs]
    inputs = sorted(inputs, key=lambda x: x[0])
    for ((s1, e1), (s2, e2)) in zip(inputs, inputs[1:]):
        if e1 >= s2:
            print('Overlap!')
            break

    # go through the ranges and check for numbers that are repeated
    for start, end in inputs:
        for num in range(start, end+1):
            result += separate_numb(str(num))

    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
