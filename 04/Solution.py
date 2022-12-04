def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            line = line.split(',')
            line = [[int(ele) for ele in lt.split('-')] for lt in line]
            inputs.append(line)
    return inputs


def main1():
    result = 0

    # get the input from the file
    lines = read_input()

    # split the lines into pairs

    # contained in function
    result = sum((line[0][0] >= line[1][0] and line[0][1] <= line[1][1])
                 or (line[1][0] >= line[0][0] and line[1][1] <= line[0][1]) for line in lines)

    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # get the input from the file
    lines = read_input()

    # contained in function
    result = sum(line[1][0] <= line[0][0] <= line[1][1] or line[0][0] <= line[1][0] <= line[0][1] for line in lines)

    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
