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


def golfing_main1():
    print(sum(map(lambda x: (x[2] <= x[0] and x[1] <= x[3]) or (x[0] <= x[2] and x[3] <= x[1]), (list(map(int, line.rstrip().replace('-', ',').split(','))) for line in open('input.txt').readlines()))))


def golfing_main2():
    print(sum(map(lambda x: (x[2] <= x[0] <= x[3]) or (x[0] <= x[2] <= x[1]),(list(map(int, line.rstrip().replace('-', ',').split(','))) for line in open('input.txt').readlines()))))


if __name__ == '__main__':
    main1()
    main2()
    golfing_main1()
    golfing_main2()
