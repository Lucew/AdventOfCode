def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def dirty_quick(line: str, window_length: int):
    for idx, ch in enumerate(line[:-window_length]):
        if len(set(line[idx:idx+window_length])) == window_length:
            return idx + window_length


def main1():
    inputs = read_input()
    for ldx, line in enumerate(inputs):
        idx = dirty_quick(line, window_length=4)
        print(f'The result for  solution 1 line {ldx} is: {idx}')


def main2():
    inputs = read_input()
    for ldx, line in enumerate(inputs):
        idx = dirty_quick(line, window_length=14)
        print(f'The result for  solution 2 line {ldx} is: {idx}')


if __name__ == '__main__':
    main1(1)
    main2()
