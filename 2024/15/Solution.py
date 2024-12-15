import collections
import heapq
import functools
import bisect
import sortedcontainers


def read_input(path: str = 'input.txt'):
    mapped = []
    inputs = []
    switch = False
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            if not line:
                switch = True
            if switch:
                inputs.append(line)
            else:
                mapped.append(list(line))
    inputs = "".join(inputs)
    return mapped, inputs


def pretty_print(mapped: list[list[str]]):
    for line in mapped:
        print("".join(line))


def elements_to_map(row_elements: dict[str:collections.defaultdict[int:int]], m, n, position: None | list[int, int] = None):
    mapped = [['.']*n for _ in range(m)]
    for rx, cxs in row_elements['O'].items():
        for cx in cxs:
            mapped[rx][cx] = 'O'
    for rx, cxs in row_elements['#'].items():
        for cx in cxs:
            mapped[rx][cx] = '#'
    if position is not None:
        mapped[position[0]][position[1]] = '@'
    return mapped


def main1(debug: bool = False):

    # get the input
    mapped, inputs = read_input()
    m = len(mapped)
    n = len(mapped[0])

    # go through the input and get chests and wall per row and column
    row_elements = {'O': collections.defaultdict(sortedcontainers.SortedList), '#': collections.defaultdict(sortedcontainers.SortedList)}
    col_elements = {'O': collections.defaultdict(sortedcontainers.SortedList), '#': collections.defaultdict(sortedcontainers.SortedList)}
    elements = [row_elements, col_elements]
    position = [0, 0]
    for rx, row in enumerate(mapped):
        for cx, ele in enumerate(row):
            if ele == '@':
                position = [rx, cx]
            elif ele == '.':
                continue
            else:
                row_elements[ele][rx].add(cx)
                col_elements[ele][cx].add(rx)

    # go through the steps from the inputs
    dir_translator = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
    for step_dx, direction in enumerate(inputs):
        if debug:
            print(f'Step {step_dx} Direction:', direction)
            pretty_print(elements_to_map(row_elements, m, n, position))

        # get the next wall position
        updater = dir_translator[direction]

        # get the position we will update
        # 0 if movement in column direction (up-down)
        # 1 if movement in row direction (left-right)
        update_dx = 0 if updater[0] != 0 else 1

        # get the correct direction walls and boxes
        walls = elements[1-update_dx]['#'][position[1-update_dx]]
        boxes = elements[1-update_dx]['O'][position[1-update_dx]]
        if debug:
            print('Walls, Boxes and position:')
            print(walls, boxes, position[update_dx])

        # we need to search walls smaller than us and boxes smaller than us, but bigger than the wall
        if sum(updater) < 0:
            if debug:
                print('Go left/up')
            # get the next wall
            wdx = walls.bisect(position[update_dx])-1

            # get the next box to us and to the wall
            bdx = boxes.bisect(position[update_dx])-1
            before_wall_bdx = boxes.bisect(walls[wdx])

            # check for free spaces by counting the boxes between us and the wall
            boxes_number = bdx-before_wall_bdx+(before_wall_bdx >= 0)
            steps_to_wall = position[update_dx]-walls[wdx]-1

        else:  # go
            if debug:
                print('Go right/down')
            # get the next wall
            wdx = walls.bisect(position[update_dx])

            # get the next box to us and to the wall
            bdx = boxes.bisect(position[update_dx])
            before_wall_bdx = boxes.bisect(walls[wdx])-1

            # check for free spaces by counting the boxes between us and the wall
            boxes_number = max(before_wall_bdx-bdx+(bdx < len(boxes)), 0)
            steps_to_wall = walls[wdx]-position[update_dx]-1

        # we can only update if there is steps to the wall and a free space
        if debug:
            print('Steps to Wall, Walls, Next Wall Index')
            print(steps_to_wall, walls, wdx)
            print('Boxes to Wall, Walls, Next Box Index, Box before Wall index')
            print(boxes_number, boxes, bdx, before_wall_bdx)
        if steps_to_wall > boxes_number:
            # update our position
            position[update_dx] += updater[update_dx]

            # get the stack of boxes we have to update
            curr_dx = position[update_dx]
            updatable_boxes = []
            if debug:
                print(bdx, boxes, curr_dx)
            while 0 <= bdx < len(boxes) and curr_dx == boxes[bdx]:
                updatable_boxes.append(bdx)
                curr_dx += updater[update_dx]
                bdx += updater[update_dx]
            if debug:
                print(updatable_boxes)
            # update the boxes
            other_boxes = elements[update_dx]['O']
            other_idx = position[1-update_dx]
            for bx in updatable_boxes:

                # update the own dictionary
                bdx = boxes.pop(bx)
                boxes.add(bdx+updater[update_dx])
                if debug:
                    print(boxes, bdx)

                # update the other dictionary boxes
                other_boxes[bdx].remove(other_idx)
                other_boxes[bdx+updater[update_dx]].add(other_idx)
        if debug:
            print()
    print(f'The result for solution 1 is: {sum(rx*100 + cx for rx, boxes in row_elements["O"].items() for cx in boxes)}')


def extend_input(mapped: list[list[str]], m, n):
    new_mapped = [[""]*n*2 for _ in range(m)]
    position = [0, 0]
    for rx, row in enumerate(mapped):
        for cx, ele in enumerate(row):
            if ele == '@':
                new_mapped[rx][cx*2] = '@'
                new_mapped[rx][cx*2+1] = '.'
                position = [rx, cx*2]
            elif ele == 'O':
                new_mapped[rx][cx * 2] = '['
                new_mapped[rx][cx * 2 + 1] = ']'
            else:
                new_mapped[rx][cx * 2] = ele
                new_mapped[rx][cx * 2 + 1] = ele
    return position, new_mapped


def main2(debug: bool = False):
    result = 0

    # get the input
    mapped, inputs = read_input()
    m = len(mapped)
    n = len(mapped[0])

    # extend the input
    position, mapped = extend_input(mapped, m, n)
    n = n*2

    # go through the directions
    # go through the steps from the inputs
    dir_translator = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
    for step_dx, direction in enumerate(inputs):
        if debug:
            print(f'Step {step_dx} Direction:', direction)
            pretty_print(mapped)

        # get the current direction we want to go in
        updater = dir_translator[direction]

        # go recursively until we meet either a free space or a wall
        # then we backtrack
        shift_allowed = check_shift(position[0], position[1], mapped, updater, debug)
        if shift_allowed:
            if debug:
                print('WE CAN SHIFT')
            position[0], position[1] = make_shift(position[0], position[1], mapped, updater, debug)
        if debug:
            print()
    if debug:
        pretty_print(mapped)
    print(f'The result for solution 2 is: {sum(rx*100+cx for rx, row in enumerate(mapped) for cx, ele in enumerate(row) if ele == "[")}')


def check_shift(rx, cx, mapped: list[list[str]], updater, debug):

    # end recursion if free space or wall
    if mapped[rx][cx] == '#':
        if debug:
            print(rx, cx, 'Met wall.')
        return False
    if mapped[rx][cx] == '.':
        if debug:
            print(rx, cx, 'Met free space.')
        return True

    # update the position (we can now only meet boxes)
    nrx, ncx = rx + updater[0], cx + updater[1]

    if mapped[rx][cx] == '@':
        shift_allowed = check_shift(nrx, ncx, mapped, updater, debug)
        return shift_allowed

    # if we go into column direction (up/down), we need to add the additional position
    if updater[0]:
        if debug:
            print(rx, cx, 'Met Box in column direction.')
        shift = -1 if mapped[rx][cx] == ']' else 1
        shift_allowed = check_shift(nrx, ncx, mapped, updater, debug) and check_shift(nrx, ncx+shift, mapped, updater, debug)
    # if we go into row direction (left/right), we need to add the additional position
    else:
        if debug:
            print(rx, cx, 'Met Box in row direction.')
        shift_allowed = check_shift(nrx, ncx+updater[1], mapped, updater, debug)
    return shift_allowed


def make_shift(rx, cx, mapped: list[list[str]], updater, debug):

    # end recursion if free space or wall
    if mapped[rx][cx] == '#':
        if debug:
            print(rx, cx, 'Met wall.')
        return False
    if mapped[rx][cx] == '.':
        if debug:
            print(rx, cx, 'Met free space.')
        return True

    # update the position (we can now only meet boxes)
    nrx, ncx = rx + updater[0], cx + updater[1]

    if mapped[rx][cx] == '@':
        make_shift(nrx, ncx, mapped, updater, debug)
        mapped[nrx][ncx] = '@'
        mapped[rx][cx] = '.'
        return nrx, ncx

    # if we go into column direction (up/down), we need to add the additional position
    if updater[0]:
        if debug:
            print(rx, cx, 'Met Box in column direction.')
        shift = -1 if mapped[rx][cx] == ']' else 1
        make_shift(nrx, ncx, mapped, updater, debug)
        make_shift(nrx, ncx + shift, mapped, updater, debug)
    # if we go into row direction (left/right), we need to add the additional position
    else:
        if debug:
            print(rx, cx, 'Met Box in row direction.')
        make_shift(nrx, ncx + updater[1], mapped, updater, debug)

    # shift in column direction (up/down)
    if updater[0]:
        shift = -1 if mapped[rx][cx] == ']' else 1
        if debug:
            print(nrx, ncx, shift, mapped[nrx][ncx], mapped[nrx][ncx+shift])
        mapped[nrx][ncx] = mapped[rx][cx]
        mapped[nrx][ncx+shift] = mapped[rx][cx+shift]
        mapped[rx][cx] = '.'
        mapped[rx][cx+shift] = '.'

    # shift in row direction (left/right)
    else:
        mapped[nrx][ncx+updater[1]] = mapped[rx][cx+updater[1]]
        mapped[nrx][ncx] = mapped[rx][cx]
        mapped[rx][cx] = '.'
    return nrx, ncx


if __name__ == '__main__':
    main1()
    main2(False)
