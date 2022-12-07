from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip().split(' ')
            inputs.append(line)
    return inputs


def main1():
    file_system = dict()
    stack = []
    inputs = read_input()
    for line in inputs:
        # check the command
        # change directory
        if line[0] == '$' and line[1] == 'cd':
            if line[2] == '/':
                stack.clear()
                stack.append('/')
            elif line[2] == '..':
                if stack[-1] != '/':
                    stack.pop()
            else:
                stack.append(line[2])

        elif line[0].isnumeric():

            # go through the stack and create dict
            cur_path = file_system
            for idx, ele in enumerate(stack):

                # add element to the file system
                if ele not in cur_path:
                    cur_path[ele] = {'sub': dict(), 'files': [0]}

                # go further
                if idx == len(stack) - 1:
                    cur_path = cur_path[ele]
                else:
                    cur_path = cur_path[ele]['sub']

            # append the file size
            cur_path['files'].append(int(line[0]))

    # go through the file system and add up
    def recursive_walk(folder):

        # get folder size
        disc_space = sum(folder['files'])

        # check whether the folder is empty
        if len(folder['sub']) == 0:
            return disc_space, disc_space if disc_space <= 100000 else 0

        # go deeper
        accumulated_space = 0
        for sub in folder['sub'].values():
            sub_space, sub_smaller = recursive_walk(sub)

            # add up the disc space
            disc_space += sub_space
            accumulated_space += sub_smaller

        return disc_space, accumulated_space + disc_space if disc_space <= 100000 else accumulated_space

    result = recursive_walk(file_system['/'])[1]
    print(f'The result for solution 1 is: {result}')


def main2():

    # make the file system
    file_system = dict()
    stack = []
    inputs = read_input()
    for line in inputs:
        # check the command
        # change directory
        if line[0] == '$' and line[1] == 'cd':
            if line[2] == '/':
                stack.clear()
                stack.append('/')
            elif line[2] == '..':
                if stack[-1] != '/':
                    stack.pop()
            else:
                stack.append(line[2])

        elif line[0].isnumeric():

            # go through the stack and create dict
            cur_path = file_system
            for idx, ele in enumerate(stack):

                # add element to the file system
                if ele not in cur_path:
                    cur_path[ele] = {'sub': dict(), 'files': [0]}

                # go further
                if idx == len(stack) - 1:
                    cur_path = cur_path[ele]
                else:
                    cur_path = cur_path[ele]['sub']

            # append the file size
            cur_path['files'].append(int(line[0]))

    # go through the file system and add up
    def recursive_walk(folder, current_path, folder_sizes):

        # get the sum of files
        disc_space = sum(folder['files'])

        # check whether the folder is empty
        if len(folder['sub']) == 0:
            # add the folder size to the outer scope dict
            folder_sizes["/".join(current_path)] = disc_space

            return disc_space, disc_space if disc_space <= 100000 else 0

        # go deeper
        accumulated_space = 0
        for name, sub in folder['sub'].items():

            # append the curren name to the path
            current_path.append(name)

            # go recursively
            sub_space, sub_smaller = recursive_walk(sub, current_path, folder_sizes)

            # delete the name from the path
            current_path.pop()

            # add up the disc space
            disc_space += sub_space
            accumulated_space += sub_smaller

        # add the folder size to the outer scope dict
        folder_sizes["/".join(current_path)] = disc_space

        return disc_space, accumulated_space + disc_space if disc_space <= 100000 else accumulated_space

    # a variable to save the folder size
    sizes = dict()
    result = recursive_walk(file_system['/'], ['/'], sizes)[0]

    # check the amount we need to free
    need_to_free = 30000000 - (70000000 - result)

    # go through the sizes and find the smallest one larger than the space we need to free
    min_space = 70000000
    for value in sizes.values():
        if value > need_to_free:
            min_space = min(min_space, value)

    print(f'The result for solution 2 is: {min_space}')


if __name__ == '__main__':
    main1()
    main2()
