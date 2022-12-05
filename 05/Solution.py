def read_input(path: str = 'input.txt'):
    with open(path) as filet:

        # get the crates on the ship
        crates = []
        line = ' '
        while line:

            # get the line
            line = filet.readline().rstrip()

            # check for empty line
            if not line:
                break

            line = list(line[1::4])
            crates.append(line)

        # restructure the crates
        tmp = [[] for _ in range(len(crates[-1]))]
        for line in crates[:-1]:
            for idx, ele in enumerate(line):
                if ele != ' ':
                    tmp[idx].append(ele)
        crates = [list(reversed(stack)) for stack in tmp]

        # get the commands
        commands = []
        for line in filet.readlines():
            line = line.rstrip()
            commands.append(list(int(ele) for ele in line.split()[1::2]))

    return crates, commands


def main1():

    # get the input
    crates, instructions = read_input()

    # go through the instructions
    for number, source, target in instructions:

        # extend the target
        crates[target-1].extend(reversed(crates[source-1][-number:]))

        # delete the source
        crates[source-1] = crates[source-1][:-number]

    print(f'The result for solution 1 is: {"".join(ele[-1] for ele in crates)}')


def main2():

    # get the input
    crates, instructions = read_input()

    # go through the instructions
    for number, source, target in instructions:
        # extend the target
        crates[target - 1].extend(crates[source - 1][-number:])

        # delete the source
        crates[source - 1] = crates[source - 1][:-number]

    print(f'The result for solution 1 is: {"".join(ele[-1] for ele in crates)}')


if __name__ == '__main__':
    main1()
    main2()
