import collections


def read_input(path: str = 'input.txt') -> set[tuple[int, int]]:
    inputs = set()
    with open(path) as filet:
        for rx, line in enumerate(filet.readlines()):
            line = line.rstrip()
            inputs.update((rx, cx) for cx, ele in enumerate(line) if ele == '#')
    return inputs


def scan_surrounding(rx: int, cx: int, elves: set[tuple[int, int]]) -> tuple[list[int, int, int, int], bool]:

    # make an array for surrounding elves
    # north, south, west, east
    surr = [0]*4
    somebody = False

    for (nrx, ncx) in ((rx+1, cx), (rx-1, cx), (rx, cx+1), (rx, cx-1), (rx+1, cx+1),
                       (rx-1, cx-1), (rx+1, cx-1), (rx-1, cx+1)):
        if (nrx, ncx) in elves:

            # elf is north
            surr[0] += nrx < rx
            # elf is south
            surr[1] += nrx > rx
            # elf is west
            surr[2] += ncx < cx
            # elf is east
            surr[3] += ncx > cx

            # we met an elf!
            somebody = True
    return surr, somebody


def planned_position(rx, cx, surrounding_elves: list[int, int, int, int], direction_pointer, has_neighbour):

    # check whether our elf will not be moving
    if not has_neighbour:
        return rx, cx, True

    for idx in range(direction_pointer, direction_pointer + 4):

        # make pointer module to stay in scope of the four directions
        nidx = idx % 4

        # we have an empty direction
        if surrounding_elves[nidx] == 0:

            # mark that our elf needs to move

            # empty direction is north
            if nidx == 0:
                nrx = rx - 1
                ncx = cx

            # is south
            elif nidx == 1:
                nrx = rx + 1
                ncx = cx

            # is west
            elif nidx == 2:
                nrx = rx
                ncx = cx - 1

            # is east
            elif nidx == 3:
                nrx = rx
                ncx = cx + 1

            else:
                raise NotImplementedError
            break
    else:
        # elf can't move
        nrx = rx
        ncx = cx
    return nrx, ncx, False


def pretty_print(elves: set[tuple[int, int]], round_number: int = -1):
    min_rx = min(coords[0] for coords in elves)
    max_rx = max(coords[0] for coords in elves)

    min_cx = min(coords[1] for coords in elves)
    max_cx = max(coords[1] for coords in elves)
    print(f'==================== ROUND {round_number} ====================')
    for rx in range(min_rx, max_rx+1):
        for cx in range(min_cx, max_cx+1):
            if (rx, cx) in elves:
                print('#', end='')
            else:
                print('.', end='')
        print()


def main1(rounds=10):

    # get the input from the elves
    elves = read_input()

    # importance pointer for which direction to look at first
    direction_pointer = 3

    # go for for some rounds
    rdx = 0
    for rdx in range(rounds):

        # make a dict in order to check which position is
        # not occupied
        occupied = collections.defaultdict(list)

        # update the direction pointer
        direction_pointer = (direction_pointer + 1) % 4

        # make a counter to count how many elves are static
        static_elves = 0

        # go through each of the elves
        for rx, cx in elves:

            # scan the surrounding
            # [north, south, west, east]
            surr, has_neighbour = scan_surrounding(rx, cx, elves)

            # check for a place to move to according to our current priority
            nrx, ncx, is_static = planned_position(rx, cx, surr, direction_pointer, has_neighbour)
            static_elves += is_static

            # check whether we collide with an elf
            occupied[(nrx, ncx)].append((rx, cx))

        # make the new elves position set
        elves = set()
        for ncoords, old_coords in occupied.items():
            if len(old_coords) == 1:
                elves.add(ncoords)
            else:
                elves.update(old_coords)

        # visualize the elves
        # pretty_print(elves, rdx)

        # check if we moved any elves
        # print(static_elves, len(elves))
        if static_elves == len(elves):
            break

    # in order to compute the rectangle we need the (max_rx, min_cx) and (min_rx, max_cx) points of the elves
    min_rx = min(coords[0] for coords in elves)
    max_rx = max(coords[0] for coords in elves)

    min_cx = min(coords[1] for coords in elves)
    max_cx = max(coords[1] for coords in elves)

    # compute the rectangle area minus the elves
    result = (max_rx-min_rx+1)*(max_cx-min_cx+1) - len(elves)
    print(f'The result for solution 1 is: {result}')
    return rdx


def main2():
    result = main1(1_000) + 1
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
