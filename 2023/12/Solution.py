import functools
import itertools
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


# we could try to solve this recursively by just setting possible positions
def recursive_solve(rdx1, rdx2, cache, repr1, repr2, layer=0, debug=False):

    # skip positions where there can be no start
    while rdx1 < len(repr1) and repr1[rdx1] == '.':
        rdx1 += 1

    # check whether we have the position in the cache already
    if (rdx1, rdx2) in cache:
        return cache[(rdx1, rdx2)]

    # check whether we are finished with all the expected groups
    if rdx2 >= len(repr2):

        # check whether there are no known damages left
        cache[(rdx1, rdx2)] = int(all(ele != "#" for ele in repr1[rdx1:]))
        return cache[(rdx1, rdx2)]

    # get the group size for better readability
    group_size = repr2[rdx2]

    # make a function to check a valid group
    def check_valid(symbol_cnt, start_index, group_size_expected):
        return (symbol_cnt == group_size_expected
                and ((start_index+group_size_expected) >= len(repr1) or repr1[start_index+group_size_expected] != "#"))

    # collect the possible starting points for the current group by using a sliding window
    sliding_window_cnt = sum(ele != "." for ele in repr1[rdx1:rdx1+group_size])
    possible_starts = [rdx1] if check_valid(sliding_window_cnt, rdx1, group_size) else []
    for start, ele in enumerate(repr1[rdx1+group_size:], rdx1+1):
        # we need to break when
        #
        # We find a known broken spring as this forces us to start there at the latest
        # We need more possible symbols left as the current group and our group require
        # There are more groups necessary than we have groups left
        if repr1[start-1] == "#" or cache["required"][rdx2] > cache["possible_symbols"][start]:
            break

        sliding_window_cnt -= int(repr1[start-1] != ".")
        sliding_window_cnt += int(ele != ".")

        # check whether sliding window has enough elements to fit the group and is at the end
        # or can place "." after the window
        if check_valid(sliding_window_cnt, start, group_size):
            possible_starts.append(start)
    if debug:
        print(f"{layer*'--------'}", f"Possible starting points for for group {rdx2}[N={group_size}]: {possible_starts}")

    # go through the possible starts and jump to the next start
    return_val = 0
    for start in possible_starts:
        if debug:
            print(f"{layer * '--------'}", f"Group {rdx2}[N={group_size}] from {start}:{start+group_size}")
        return_val += recursive_solve(start+group_size+1, rdx2+1, cache, repr1, repr2, layer+1)
    if debug:
        print(f"{layer*'--------'}", return_val)

    # save into the cache
    cache[(rdx1, rdx2)] = return_val
    return return_val


def main1(debug=False, factor=1):
    result = 0

    # go through every line as they are independent riddles
    for ldx, line in enumerate(read_input()):

        # parse the line into the two input formats
        repr1, repr2 = line.split(" ")

        # apply the factor
        repr1 = "?".join([repr1]*factor)
        repr2 = ",".join([repr2]*factor)

        # parse the repr2 into numbers
        repr2 = [int(ele) for ele in repr2.split(",")]

        # make a cache for the function
        cache = dict()

        # put some additional information for faster termination into the cache
        possible_symbols = 0
        symbols_left = [0]*len(repr1)
        for idx, ele in enumerate(reversed(repr1), 1):
            possible_symbols += int(ele != '.')
            symbols_left[-idx] = possible_symbols
        cache["possible_symbols"] = symbols_left  # how many non-functioning springs can there be with and after here
        required_left = [0]*len(repr2)
        required = 0
        for idx, num in enumerate(reversed(repr2), 1):
            required += num
            required_left[-idx] = required
        cache["required"] = required_left  # how many non-functioning springs do we still need

        # call the recursive function
        if debug:
            print()
            print(f"Begin Line {ldx}: {repr1} with groups: {repr2}")
        line_res = recursive_solve(0, 0, cache, repr1, repr2, debug=debug)

        if debug:
            print(f"Line {ldx}: {line_res}")
        result += line_res

    if factor == 1:
        print(f'The result for solution 1 is: {result}')
    else:
        return result


def main2(debug=False):
    print(f'The result for solution 2 is: {main1(debug, 5)}')


if __name__ == '__main__':
    main1()
    main2()
