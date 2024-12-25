import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    keys = []
    locks = []
    is_lock = -1
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()

            # check whether it is an empty line
            if not line:
                is_lock = -1
                continue

            # check whether we currently are in unknown territory
            if is_lock == -1:
                if line[0] == '#':
                    is_lock = 1
                    locks.append([])
                else:
                    is_lock = 0
                    keys.append([])


            # build the keys and the locks
            if is_lock == 1:
                locks[-1].append(line)
            else:
                keys[-1].append(line)

    return locks, keys


def main1():
    result = 0

    # get the locks and the keys
    locks, keys = read_input()

    # go through the keys and put them into their respective lists
    sorted_keys = {ele: [] for ele in range(len(keys[0][0]))}

    # go through the keys and fill them in
    for kx, key in enumerate(keys):

        # find the key positions per columns
        for rx, row in enumerate(key[:-1]):
            for cx, ele in enumerate(row):
                if ele == '.' and key[rx+1][cx] == '#':
                    sorted_keys[cx].append((len(key)-rx-1, kx))

    # sort the keys
    for keys in sorted_keys.values():
        keys.sort()

    # go through the locks and check for keys that match
    for lock in locks:

        # find the lock positions per columns
        lock_positions = [0]*len(lock[0])
        for rx, row in enumerate(lock[:-1]):
            for cx, ele in enumerate(row):
                if ele == '#' and lock[rx + 1][cx] == '.':
                    lock_positions[cx] = rx+1

        # go through the keys and find all that match
        allowed_keys = set(range(len(keys)))
        for cx, lock_cx in enumerate(lock_positions):
            kdx = bisect.bisect(sorted_keys[cx], len(lock) - lock_positions[cx], key=lambda x: x[0])
            allowed_keys = allowed_keys.intersection(key[1] for key in sorted_keys[cx][:kdx])
        result += len(allowed_keys)
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0
    print(f'The result for solution 2 is: YES, WE DID IT!')


if __name__ == '__main__':
    main1()
    main2()
