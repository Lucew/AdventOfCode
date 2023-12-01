def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append([int(ele) for ele in line])
    return inputs


def check_valley(rx, cx, ele, matrix):
    if rx > 0 and matrix[rx-1][cx] <= ele:
        return False
    elif rx < len(matrix) - 1 and matrix[rx+1][cx] <= ele:
        return False
    elif cx > 0 and matrix[rx][cx-1] <= ele:
        return False
    elif cx < len(matrix[0]) - 1 and matrix[rx][cx+1] <= ele:
        return False
    return True


def main1():
    result = 0

    # get the input
    matrix = read_input()

    # traverse the matrix
    for rx, row in enumerate(matrix):
        for cx, ele in enumerate(row):
            result += check_valley(rx, cx, ele, matrix)*(ele+1)

    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()