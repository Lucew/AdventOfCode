def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def snafu2digit(snafu_digit: str):
    if snafu_digit.isdigit():
        return int(snafu_digit)
    elif snafu_digit == '-':
        return -1
    elif snafu_digit == '=':
        return -2
    else:
        # Sanity checking
        raise NotImplementedError


def snafu2number(snafu_number: str):
    current = 0
    for ch in snafu_number:
        current *= 5
        current += snafu2digit(ch)
    return current


def number2snafu(number: int):
    snafu = []
    translation = {-2: '=', -1: '-'}
    while number:
        number, res = divmod(number, 5)
        if res == 3:
            number += 1
            res = -2
        elif res == 4:
            number += 1
            res = -1
        snafu.append(res)
    print("".join([str(digit) if digit >= 0 else translation[digit] for digit in reversed(snafu)]))


def main1():
    # get the inputs
    inputs = read_input()

    # go through each of the snafu numbers and add up
    result = sum(snafu2number(snafu_number) for snafu_number in inputs)
    number2snafu(result)

    # add in snafu numbers
    print(str())
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
