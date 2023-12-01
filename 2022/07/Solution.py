import collections


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip().split(' ')
            inputs.append(line)
    return inputs


def create_filesystem(instructions: list):

    # introduce a dict that we will use for the file systems
    file_system = dict()

    # introduce a stack that we will use for the current path
    stack = collections.deque()

    # go through the instructions one by one
    for line in instructions:

        # search for change directory commands that start with $ cd
        if line[0] == '$' and line[1] == 'cd':

            # check for return to highest level
            if line[2] == '/':

                # clear the stack
                stack.clear()

                # set us to the highest level
                stack.append('/')

            # check for level up command
            elif line[2] == '..':

                # check that we are not already at the highest level
                if stack[-1] != '/':
                    # delete the last element from the stack
                    stack.pop()
            else:
                stack.append(line[2])

        # check for a line that has file sizes in it
        elif line[0][0].isdigit():

            # go through the file system and add the new files
            cur_path = file_system
            for idx, ele in enumerate(stack):

                # initialize the current level if we have not yet visited
                if ele not in cur_path:

                    # every directory has two parts: the subdirectories and the files
                    # at this level
                    cur_path[ele] = {'sub': dict(), 'files': {'/': 0}}

                # check whether we reached the end of our stack
                if idx == len(stack) - 1:
                    cur_path = cur_path[ele]

                # update our filesystem to the current level
                else:
                    cur_path = cur_path[ele]['sub']

            # append the file size
            cur_path['files'][line[1]] = int(line[0])

    return file_system


# go through the file system and add up
def recursive_walk(folder, current_path, folder_sizes, max_size):

    # get the space of all files at the current folder level
    folder_size = sum(folder['files'].values())

    # check whether the folder has not further subdirectories
    # so we can return
    if len(folder['sub']) == 0:

        # add the folder size to our list of folder sizes
        folder_sizes["/".join(current_path)] = folder_size

        # return the folder space and start accumulation of folders
        # bigger than the specified max_size
        return folder_size, folder_size if folder_size <= max_size else 0

    # we have subdirectories so we need to recurse deeper first
    accumulated_smaller = 0
    for name, sub in folder['sub'].items():

        # append the current name to the current path
        current_path.append(name)

        # go recursively
        sub_space, sub_smaller = recursive_walk(sub, current_path, folder_sizes, max_size)

        # reset the current path
        current_path.pop()

        # accumulate overall folder_size with subdirectories and space of folders smaller than max_size
        folder_size += sub_space
        accumulated_smaller += sub_smaller

    # add the current accumulated folder size to the outer scope dict
    folder_sizes["/".join(current_path)] = folder_size

    return folder_size, accumulated_smaller + folder_size if folder_size <= max_size else accumulated_smaller


def main1():

    # get the instructions
    instructions = read_input()

    # get the filesystem
    file_system = create_filesystem(instructions)

    # walk the filesystem
    folder_sizes = dict()
    current_path = collections.deque(['/'])
    disc_space, accumulated_smaller = recursive_walk(file_system['/'], current_path, folder_sizes, 100000)
    print(f'The result for solution 1 is: {accumulated_smaller}')


def main2():

    # get the instructions
    instructions = read_input()

    # get the filesystem
    file_system = create_filesystem(instructions)

    # walk the filesystem
    folder_sizes = dict()
    current_path = collections.deque(['/'])
    disc_space, accumulated_smaller = recursive_walk(file_system['/'], current_path, folder_sizes, 100000)

    # check the amount we need to free
    max_space = 70_000_000
    needed_space = 30_000_000
    need_to_free = needed_space - (max_space - disc_space)

    # go through the sizes and find the smallest one larger than the space we need to free
    min_space = max_space
    for value in folder_sizes.values():
        if value > need_to_free:
            min_space = min(min_space, value)

    print(f'The result for solution 2 is: {min_space}')


if __name__ == '__main__':
    main1()
    main2()
