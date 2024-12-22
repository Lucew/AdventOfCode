import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(int(line))
    return inputs


@functools.cache
def process_number(num):
    # make the modulo operation as and
    mod = (2**24)-1

    # multiply with 64
    num = ((num << 6)^num) & mod

    # divide by 32
    num = ((num >> 5)^num) & mod

    # multiply with 2048
    num = ((num << 11)^num) & mod
    return num


def main1():
    result = 0

    # get the input
    numbers = read_input()

    for num in numbers:
        for _ in range(2000):
            num = process_number(num)
        result += num
    print(f'The result for solution 1 is: {result}')


def main2():

    # get the input
    numbers = read_input()

    # get the sequences for each buyer
    sequences = []
    for num in numbers:
        curr_seq = []
        prev = num
        for _ in range(2000):
            num = process_number(num)
            curr_seq.append(((num % 10) - (prev % 10), num % 10))
            prev = num
        sequences.append(curr_seq)

    # go through the sequences and count bananas
    banana = collections.defaultdict(int)
    for curr_seq in sequences:

        # make a pointer through the sequences and only keep the first occurrence!
        curr_banana = dict()
        for seq_start, (_, cost) in enumerate(curr_seq[3:]):
            curr_tuple = tuple(ele[0] for ele in curr_seq[seq_start: seq_start+4])
            if curr_tuple not in curr_banana:
                curr_banana[curr_tuple] = cost

        # update the banana
        for key, val in curr_banana.items():
            banana[key] += val

    # get the maximum bananas, that we can get
    print(f'The result for solution 2 is: {max(banana.values())}')


if __name__ == '__main__':
    main1()
    main2()
