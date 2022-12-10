def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            line = line.split(' ')
            if len(line) == 1:
                inputs.append([line[0], 0])
            else:
                inputs.append(['noop', 0])
                inputs.append([line[0], int(line[1])])
    return inputs


def main1():
    result = 0

    # get the inputs
    inputs = read_input()

    # go through the inputs
    x_register = 1
    for cycle, (instruction, value) in enumerate(inputs, 1):

        # make the cycle check
        if (cycle + 20) % 40 == 0:
            result += x_register*cycle

        # update the signal
        x_register += value

    print(f'The result for solution 1 is: {result}')


def main2():

    # get the inputs
    inputs = read_input()

    # get the screen
    screen = [['.']*40 for _ in range(6)]

    # go through the inputs
    x_register = 1
    for cycle, (instruction, value) in enumerate(inputs, 1):

        # check whether cycle is value of x register minus one/ equal / plus one
        rx, cx = divmod(cycle-1, 40)
        if x_register - 1 <= cx <= x_register + 1:
            screen[rx][cx] = '#'

        # update the signal
        x_register += value

    print('The result for solution 2 is:')
    for row in screen:
        for ele in row:
            print(ele, end=' ')
        print()


if __name__ == '__main__':
    main1()
    main2()
