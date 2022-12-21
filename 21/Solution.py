import re
import math


FUNCTIONS = {'-': lambda x, y: x - y, '*': lambda x, y: x * y, '+': lambda x, y: x + y, '/': lambda x, y: x / y,
             '=': lambda x, y: x == y}


def read_input(path: str = 'input.txt'):
    inputs = dict()
    with open(path) as filet:
        for line in filet.readlines():

            # strip any spaces oor new lines
            line = line.rstrip()

            # split the line at the colon
            line = line.split(': ')

            # check whether part 2 is a number
            if line[1].isnumeric():
                line[1] = int(line[1])
            else:
                line[1] = line[1].split(' ')
                line[1] = [int(line[1][0]) if line[1][0].isnumeric() else line[1][0],
                           FUNCTIONS[line[1][1]],
                           int(line[1][2]) if line[1][2].isnumeric() else line[1][2]]

            inputs[line[0]] = line[1]
    return inputs


def dfs(monkey: str, graph: dict[str: list]):

    # check whether the monkey yells a number
    if isinstance(graph[monkey], int) or isinstance(graph[monkey], float):
        return graph[monkey]

    # compute the result of this monkey
    monkey_number = graph[monkey][1](dfs(graph[monkey][0], graph), dfs(graph[monkey][2], graph))

    # replace this monkeys number
    graph[monkey] = monkey_number

    return monkey_number


def main1():

    # load the input
    monkeys = read_input()

    # start a graph traversal from the root
    result = dfs('root', monkeys)
    print(f'The result for solution 1 is: {result}')


def read_input2(path: str = 'input.txt'):
    inputs = dict()
    with open(path) as filet:
        for line in filet.readlines():
            # strip any spaces oor new lines
            line = line.rstrip()

            # split the line at the colon
            line = line.split(': ')

            # add to the dict
            inputs[line[0]] = line[1]
    return inputs


def dfs2(monkey, graph):

    # check whether we reached the human
    if monkey == 'humn':
        return 'humn'

    # check whether the monkey yells a number
    if graph[monkey].isnumeric():
        return int(graph[monkey])
    elif isinstance(graph[monkey], int) or isinstance(graph[monkey], float):
        return graph[monkey]

    # split the current string
    operations = graph[monkey].split(' ')

    # get the result of the left monkey
    left = dfs2(operations[0], graph)

    # get the result of the right monkey
    right = dfs2(operations[2], graph)

    # check whether we can compute the operation
    if (isinstance(left, float) or isinstance(left, int)) \
            and (isinstance(right, float) or isinstance(right, int)):

        # compute the result
        result = FUNCTIONS[operations[1]](left, right)
        return result
    left = str(left) if (isinstance(left, float) or isinstance(left, int) or left == 'humn') else f'({left})'
    right = str(right) if (isinstance(right, float) or isinstance(right, int) or left == 'humn') else f'({right})'
    return f'{left} {operations[1]} {right}'


def check_formula():
    # load the input
    monkeys = read_input2()

    # get the two monkeys that need to be equal
    left, right = tuple(monkey for monkey in monkeys['root'].split(' ') if monkey not in FUNCTIONS)

    # go and find the monkey values
    formula = f'{dfs2(left, monkeys)} = {dfs2(right, monkeys)}'

    # check that human is only used once (which guarantees that it is an affine function)
    assert len(re.findall('humn', formula)) == 1, 'Human is used more than once.'


def compute(value, monkeys):
    monkeys = monkeys.copy()
    monkeys['humn'] = value
    return dfs('root', monkeys)


def main2():

    # check for our assumptions that it is an affine function dependent on the human input
    check_formula()

    # read the input
    monkeys = read_input()

    # set the root monkey operation to minus
    # monkey1 = monkey2 -> monkey1 - monkey2 = 0
    monkeys['root'][1] = FUNCTIONS['-']

    # get two values (points on affine/linear function) in order to compute the offset
    # y1 = m*x1 + b
    # y2 = m*x2 + b
    #
    # -> y3 = 0 -> x3 = -b/m
    #
    # m = (x2-x1)/(y2-y1)
    # b = y1 - mx1
    #
    # -> x3 = x1 - y1 * (y2-y1)/(x2-x1)

    # set a starting point
    x1 = 0
    offset = 0

    # make several iteration since there might be rounding errors that get multiplied
    result = 1
    while compute(result, monkeys) != 0:

        # increase the offset
        offset += 10000000
        x2 = x1 + offset

        # get the y values
        y1 = compute(x1, monkeys)
        y2 = compute(x2, monkeys)

        # compute the result
        result = x1 - y1 * (x2-x1)/(y2-y1)

    # check for assumptions
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
