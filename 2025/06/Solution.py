import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    operations = get_operations()
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(list(int(ele) if ele.isnumeric() else operations[ele] for ele in line.split() ))
    return inputs

def read_input2(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            inputs.append(line)
    return inputs

def get_operations():
    operations = {'+': lambda x: functools.reduce(lambda y, z: y + z, x, 0),
                  '-': lambda x: functools.reduce(lambda y, z: y - z, x, 0),
                  '*': lambda x: functools.reduce(lambda y, z: y * z, x, 1)}
    return operations


def main1():
    result = 0

    # get the inputs
    inputs = read_input()

    # go through the calculations
    for idx in range(len(inputs[0])):
        result += inputs[-1][idx](tuple(inputs[ndx][idx] for ndx in range(len(inputs)-1)))
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # get the unformatted inputs and operations
    inputs = read_input2()
    operations = get_operations()

    # separate operation symbols and inputs
    operations = [operations[ele.strip()] for ele in inputs[-1].split()]
    inputs = inputs[:-1]

    # transpose the lines
    inputs = list(ele for ele in zip(*inputs))

    # go through the lines and check where we have to separate the numbers
    curr_nums = []
    opx = 0
    for ele in inputs:

        # get the current number
        currnum = 0
        was_num = False
        for char in ele:
            if char.isnumeric():
                currnum = currnum * 10 + int(char)
                was_num = True

        # check whether we still have numbers or we are finished
        if was_num:
            curr_nums.append(currnum)
        else:
            result += operations[opx](curr_nums[::-1])
            opx += 1
            curr_nums.clear()
    # deal with the last field (that was never followed by an empty column and, therefore, unprocessed)
    result += operations[opx](curr_nums[::-1])
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
