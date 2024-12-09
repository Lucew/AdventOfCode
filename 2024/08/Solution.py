from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect
import itertools


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    inputs = inputs[0]

    # go through the inputs and get (file id, start, end) and free spaces
    memory = [(0, -1, -1)]
    for idx, (file, free_space) in enumerate(itertools.zip_longest(inputs[::2], inputs[1::2], fillvalue=0)):
        memory.append([idx, memory[-1][-1]+1, memory[-1][-1]+int(file)])
        if free_space:
            memory.append([-1, memory[-1][-1]+1, memory[-1][-1]+int(free_space)])
    memory = memory[1:]

    # get the empty spaces with the first one beeing last
    empty_spaces = [ele for ele in reversed(memory) if ele[0] == -1]
    files = [ele for ele in memory if ele[0] != -1]
    return memory, files, empty_spaces

def print_memory(memory: list[tuple[int, int, int]]):
    out_str = []
    for typed, start, end in memory:
        if typed < 0:
            out_str.append('.'*(end-start+1))
        else:
            out_str.append(str(typed)*(end-start+1))
    print(''.join(out_str))


def file_sum(file_id, start, end):

    # get the sum from to
    upper = ((end+1)*end)//2
    lower = ((start-1)*start)//2
    return (upper-lower)*file_id



def main1():

    # get the memory footprint
    memory, files, empty_spaces = read_input()

    # reduce the memory until there are no more empty spaces
    finished_files = []
    while empty_spaces:

        # check that the current empty space is before us
        while empty_spaces and empty_spaces[-1][1] > files[-1][2]:
            empty_spaces.pop()
        if not empty_spaces:
            break

        # get the last block of memory and put it into the first empty space
        # print('File', files[-1], '-', empty_spaces)
        file_id, start, end = files.pop()

        # check whether the empty space is larger than our file
        e_id, e_start, e_end = empty_spaces.pop()
        if e_end-e_start > end-start:
            finished_files.append((file_id, e_start, e_start+(end-start)))
            empty_spaces.append((e_id, e_start+(end-start+1), e_end))
        elif e_end-e_start == end-start:
            finished_files.append((file_id, e_start, e_end))
        else:
            finished_files.append((file_id, e_start, e_end))
            files.append((file_id, start, end-(e_end-e_start+1)))
        # print('Files - ', files)
        # print('Empty - ', empty_spaces)
        # print('Finished - ', finished_files)
        # print()
    # print_memory(sorted(files + finished_files, key=lambda x: x[1]))
    result = sum(file_sum(*file) for file in itertools.chain(finished_files, files))
    print(f'The result for solution 1 is: {result}')


def main2():

    # get the memory footprint
    memory, files, empty_spaces = read_input()
    empty_spaces = empty_spaces[::-1]

    # reduce the memory until there are no more empty spaces
    finished_files = []
    while files:

        # get the current file
        curr_file = files.pop()
        curr_files_size = curr_file[2]-curr_file[1]

        # search the leftmost fitting free space
        min_idx = -1
        for idx, (e_id, start, end) in enumerate(empty_spaces):
            # the conditions are: 1) must fit 2) must be current best empty space 3) must be before number placement
            if end-start >= curr_files_size and (min_idx == -1 or (start < empty_spaces[min_idx][1])) and start < curr_file[1]:
                min_idx = idx
        if min_idx >= 0:
            e_id, start, end = empty_spaces[min_idx]
            finished_files.append((curr_file[0], start, start+curr_files_size))
            empty_spaces[min_idx] = (e_id, start+curr_files_size+1, end)
            empty_spaces.append((e_id, curr_file[1], curr_file[2]))
        else:
            finished_files.append(curr_file)
    result = sum(file_sum(*file) for file in itertools.chain(finished_files))
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
