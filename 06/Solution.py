from collections import Counter, defaultdict


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def solution(line: str, window_length: int):
    """
    Perfectionist solution with sliding map/set to every step is O(1) instead of O(Window_Length).

    :return: None
    """

    # initialize a dict for a sliding window
    sliding = defaultdict(int)

    # go through the characters
    idx = 0
    for idx, ch in enumerate(line):

        # guard clause for filling the dict
        if idx < window_length:
            sliding[ch] += 1
            continue

        # check whether the dict has window length
        if len(sliding) == window_length:
            break

        # add the new char
        sliding[ch] += 1

        # delete the old char if necessary
        if sliding[line[idx - window_length]] == 1:
            del sliding[line[idx - window_length]]
        else:
            sliding[line[idx - window_length]] -= 1

    return idx


def main1():
    inputs = read_input()
    for ldx, line in enumerate(inputs):
        idx = solution(line, window_length=4)
        print(f'The result for  solution 1 line {ldx} is: {idx}')


def main2():
    inputs = read_input()
    for ldx, line in enumerate(inputs):
        idx = solution(line, window_length=14)
        print(f'The result for  solution 2 line {ldx} is: {idx}')


if __name__ == '__main__':
    main1()
    main2()
