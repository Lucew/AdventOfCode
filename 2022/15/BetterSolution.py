def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()

            # get the coordinates
            coordinates = line.split(' ')
            coordinates = [int(coordinates[idx].replace(',', '').replace(':', '')[2:]) for idx in [2, 3, 8, 9]]

            # append the manhattan distance to the coordinates
            coordinates.append(abs(coordinates[0] - coordinates[2]) + abs(coordinates[1] - coordinates[3]))

            # append them to the input
            inputs.append(coordinates)
    return inputs


def is_in_range(coordinates, x, y):
    for sx, sy, bx, by, dist in coordinates:
        if abs(sx - x) + abs(sy - y) <= dist:
            return True
    return False


def main2():

    # get the coordinates
    coordinates = read_input()

    # define the possible coordinates
    max_dist = 4_000_000

    # go through the border values of all sensors
    for sx, sy, bx, by, dist in coordinates:

        # go through all rows we need to check (our row - dist - 1 or our row + dist + 1)
        # also thinking about the limits of our calculation
        for rx in range(max(0, sy - dist - 1), min(max_dist, sy + dist + 1) + 1):

            # check both columns if they are in range
            left_col = sx - (dist - abs(rx - sy)) - 1
            right_col = sx + (dist - abs(rx - sy)) + 1

            for cx in [left_col, right_col]:
                if 0 <= cx <= max_dist and not is_in_range(coordinates, cx, rx):
                    print(f'The result for solution 2 is: {cx*4_000_000 + rx}')
                    return


if __name__ == '__main__':
    import time
    t = time.time()
    main2()
    print(time.time() - t)
