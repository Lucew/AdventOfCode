from collections import defaultdict


# make a function to read the board
def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.split(' | ')[-1][:-1].split(' ')
            inputs.append(line)
    return inputs


def main1():

    # read the input
    inputs = read_input()

    # go through the input and check for unique numbers
    counter = defaultdict(int)
    for inp in inputs:
        for digit in inp:
            counter[len(digit)] += 1
    result = sum(counter[ele] for ele in [2, 4, 3, 7])
    print(f'The solution 1 is: {result}')


def main2():

    # get the inputs and outputs
    inputs = []
    outputs = []
    with open('input.txt') as filet:
        for line in filet.readlines():
            inp = line.split(' | ')[0].split(' ')
            assert len(inp) == 10
            output = line.split(' | ')[1][:-1].split(' ')
            assert len(output) == 4
            inputs.append(inp)
            outputs.append(output)

    # make a set of possible wires
    wires = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}

    # make a dict for the numbers and their respective active wires
    numbers2wires = {
        0: set(list('abcefg')),
        1: set(list('cf')),
        2: set(list('acdeg')),
        3: set(list('acdfg')),
        4: set(list('bcdf')),
        5: set(list('abdfg')),
        6: set(list('abdefg')),
        7: set(list('acf')),
        8: set(list('abcdefg')),
        9: set(list('abcdfg')),
    }
    wires2numbers = {frozenset(ele): key for key, ele in numbers2wires.items()}
    assert len(numbers2wires) == 10 and len(wires2numbers) == 10, 'Something is numbers fishy.'

    # get the symmetric differences between 0 6 and 9 (the three wires not included in one of them)
    symmetric_diff = {'c', 'd', 'e'}

    # initialize the sum
    overall_result = 0

    # go through the results and make the logical deductions
    for inp, output in zip(inputs, outputs):

        # assign the inputs to each length
        numbers = defaultdict(list)
        for num in inp:
            numbers[len(num)].append(num)

        # make some assertions
        assert [len(numbers[length]) for length in [2, 4, 3, 7, 6, 5]] == [1, 1, 1, 1, 3, 3], 'Something is fishy.'

        # make a new map for each of the elements
        mapped = {ele: set(list(wires)) for ele in wires}

        # cross out all ones
        for ch in numbers[2][0]:
            mapped[ch] = mapped[ch].intersection(numbers2wires[1])

        # cross out the fours
        for ch in numbers[4][0]:
            mapped[ch] = mapped[ch].intersection(numbers2wires[4])

        # cross out the seven
        for ch in numbers[3][0]:
            mapped[ch] = mapped[ch].intersection(numbers2wires[7])

        # get the symmetric difference of the three digits with six wires
        difference = set()
        for digit in numbers[6]:
            difference.update(wires.difference(list(digit)))
        for ch in difference:
            mapped[ch] = mapped[ch].intersection(symmetric_diff)

        # sort the items after their length
        dict_content = sorted(mapped.items(), key=lambda x: len(x[1]))
        for idx, (key, _) in enumerate(dict_content):

            # make an assertion
            assert len(mapped[key]) == 1, 'We did not cross out enough.'

            # go through the dict and cross
            for key2, setted2 in dict_content[idx+1:]:
                mapped[key2] = mapped[key2].difference(mapped[key])

        # make another assertion for the map
        assert all(len(val) == 1 for val in mapped.values())

        # make map to translator
        mapped = {key: value.pop() for key, value in mapped.items()}

        # translate the numbers we see
        result = 0
        for number in output:
            translated_number = frozenset(mapped[ch] for ch in number)
            result = result*10 + wires2numbers[translated_number]

        # get the result
        overall_result += result

    print(f'The solution 2 is: {overall_result}')


if __name__ == '__main__':
    main1()
    main2()
