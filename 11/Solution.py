from collections import deque
import functools
from heapq import heappop, heappush, heapify


def read_input(path: str = 'input.txt'):

    # read the lines
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)

    # split them by monkeys
    inputs = [inputs[idx*7:(idx+1)*7-1] for idx in range(len(inputs)//7+1)]

    # parse the outputs
    monkeys = []
    for idx, monkey in enumerate(inputs):

        # check the monkey length
        assert len(monkey) == 6, 'Monkey is too long.'

        # check the monkey number
        assert int(monkey[0].split(' ')[-1][:-1]) == idx, 'Monkey number mix up.'

        # get the list of items
        items = deque([int(ele) for ele in monkey[1].split(':')[-1].split(',')])

        # get the operation and transform it
        operation = monkey[2].split(':')[-1].split(' = ')[-1]

        # get the test
        test = monkey[3].split(': ')[-1]
        assert test.startswith('divisible by '), 'The test is not valid.'
        test = functools.partial(lambda x, y: x % y == 0, y=int(test.split(' ')[-1]))

        # get the target
        assert monkey[4].startswith('    If true: throw to monkey '), 'Target True not specified.'
        assert monkey[5].startswith('    If false: throw to monkey '), 'Target False not specified.'
        target = [int(monkey[5].split(' ')[-1]), int(monkey[4].split(' ')[-1])]
        assert target[0] != idx and target[1] != idx and 0 <= target[0] < len(inputs) and 0 <= target[1] < len(inputs), 'Monkey target are wild.'

        # build the new monkey array
        monkeys.append([items, operation, test, target])

    return monkeys


def evaluator(function: str, old: int):

    # split the function
    function = function.split(' ')

    # check for valid stuff
    assert len(function) == 3, 'Operation is not valid.'
    assert len(function[1]) == 1, 'The operation symbol is too long.'

    # check the arguments
    first = int(function[0]) if function[0].isnumeric() else old
    second = int(function[2]) if function[2].isnumeric() else old

    # get the operation
    result = 0
    if function[1] == '+':
        result = first + second
    elif function[1] == '-':
        result = first - second
    elif function[1] == '*':
        result = first * second
    else:
        raise NotImplementedError

    return result


def main1():

    # read the inputs
    inputs = read_input()

    # make a counter
    counter = [0]*len(inputs)

    # make a step
    for _ in range(20):
        for idx, monkey in enumerate(inputs):

            # go through all items the monkey has
            while monkey[0]:

                # increase inspection counter of this monkey
                counter[idx] += 1

                # get the item
                item = monkey[0].popleft()

                # calculate the new worry level (after inspection)
                worry = evaluator(monkey[1], item) // 3

                # make the check and get the target
                target = monkey[3][monkey[2](worry)]

                # throw it to the monkey
                inputs[target][0].append(worry)

    # get the k biggest apes
    biggest = get_biggest_k(counter, 2)
    print(f'The result for solution 1 is: {biggest[0]*biggest[1]}')


def get_biggest_k(nums: list, k):

    # make a heap
    heap = []

    # go through each of the numbers
    for num in nums:
        heappush(heap, num)
        while len(heap) > k:
            heappop(heap)
    return heap


def read_input2(path: str = 'input.txt'):

    # read the lines
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)

    # split them by monkeys
    inputs = [inputs[idx*7:(idx+1)*7-1] for idx in range(len(inputs)//7+1)]

    # make a set of primes
    primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}

    # parse the outputs
    monkeys = []
    for idx, monkey in enumerate(inputs):

        # check the monkey length
        assert len(monkey) == 6, 'Monkey is too long.'

        # check the monkey number
        assert int(monkey[0].split(' ')[-1][:-1]) == idx, 'Monkey number mix up.'

        # get the list of items
        items = deque([int(ele) for ele in monkey[1].split(':')[-1].split(',')])

        # get the operation and transform it
        operation = monkey[2].split(':')[-1].split(' = ')[-1]

        # get the test
        assert monkey[3].startswith('  Test: divisible by '), 'Something with the test ist off.'
        test = int(monkey[3].split(' ')[-1])
        assert test in primes, 'Test is not a prime.'

        # get the target
        assert monkey[4].startswith('    If true: throw to monkey '), 'Target True not specified.'
        assert monkey[5].startswith('    If false: throw to monkey '), 'Target False not specified.'
        target = [int(monkey[5].split(' ')[-1]), int(monkey[4].split(' ')[-1])]
        assert target[0] != idx and target[1] != idx and 0 <= target[0] < len(inputs) and 0 <= target[1] < len(inputs), 'Monkey target are wild.'

        # build the new monkey array
        monkeys.append([items, operation, test, target])

    # find the unique primes for all apes
    primes = {monkey[2] for monkey in monkeys}

    # transform all the item values into multiples of the primes
    for idx, monkey in enumerate(monkeys):

        # go through the items and make a new item list
        new_items = deque()
        for item in monkey[0]:
            new_items.append({prime: item % prime for prime in primes})

        # set the new item list
        monkeys[idx][0] = new_items

    return monkeys


def modulo_evaluator(function: str, old: int, modulo: int):

    # split the function
    function = function.split(' ')

    # check for valid stuff
    assert len(function) == 3, 'Operation is not valid.'
    assert len(function[1]) == 1, 'The operation symbol is too long.'

    # check the arguments
    first = int(function[0]) % modulo if function[0].isnumeric() else old % modulo
    second = int(function[2]) % modulo if function[2].isnumeric() else old % modulo

    # get the operation
    result = 0
    if function[1] == '+':
        result = first + second
    elif function[1] == '-':
        result = first - second
    elif function[1] == '*':
        result = first * second
    else:
        raise NotImplementedError

    return result % modulo


def main2():
    """
    The final approach is that we only need to track different modulos for every ape in order to track the passage of
    items through the apes. The absolute worry value does not matter. So we only need to keep track how the operations
    of each ape change the modulo.

    As there is a limited amount of apes (and therefore modulos) we create a dict of modulos for every ape and
    update every dict value every time we apply an operation with the rules:

    (a*b) mod c = (a mod c * b mod c) mod c
    (a+b) mod c = (a mod c + b mod c) mod c

    E.G.: We have three apes. One looks for mod3 one for mod5 one for mod7
    1) We transform every item in a dict: {3: item%3, 5: item%5, 7: item%7}
    2) For every operation we update each dict item with the rules given above
    3) We check if the right dict value is 0 if we do the passing

    :return:
    """
    # read the inputs
    inputs = read_input2()

    # make a counter
    counter = [0] * len(inputs)

    # make a step
    for _ in range(10000):
        for idx, monkey in enumerate(inputs):

            # go through all items the monkey has
            while monkey[0]:
                # increase inspection counter of this monkey
                counter[idx] += 1

                # get the item
                item = monkey[0].popleft()

                # make the calculation for every modulo value
                item = {key: modulo_evaluator(monkey[1], value, key) for key, value in item.items()}

                # get the target of the monkey
                target = monkey[3][item[monkey[2]] == 0]

                # throw it to the monkey
                inputs[target][0].append(item)

    # print the monkey counters
    # print(counter)

    # get the k biggest apes
    biggest = get_biggest_k(counter, 2)
    print(f'The result for solution 2 is: {biggest[0] * biggest[1]}')


if __name__ == '__main__':
    main1()
    main2()
