import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def main1():
    result = 0

    # get the inputs
    inputs = read_input()

    # get the starting beam
    idx = -1
    for idx, ele in enumerate(inputs[0]):
        if ele == 'S':
            break
    assert idx != -1

    # go through each line and update the splits
    beams = {idx}
    for lx, line in enumerate(inputs[1:], 1):
        new_beams = set()
        for beam in beams:
            if line[beam] == '^':
                result += 1
                new_beams.add(beam-1)
                new_beams.add(beam+1)
            else:
                new_beams.add(beam)
        # update the beams
        beams = new_beams

    print(f'The result for solution 1 is: {result}')


def main2():
    result = 1

    # get the inputs
    inputs = read_input()

    # get the starting beam
    idx = -1
    for idx, ele in enumerate(inputs[0]):
        if ele == 'S':
            break
    assert idx != -1

    # go through each line and update the splits
    beams = {idx: 1}
    for lx, line in enumerate(inputs[1:], 1):
        new_beams = collections.Counter()
        for beam, cn in beams.items():
            if line[beam] == '^':
                result += cn
                new_beams[beam-1] += cn
                new_beams[beam+1] += cn
            else:
                new_beams[beam] += cn
        # update the beams
        beams = new_beams

    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
