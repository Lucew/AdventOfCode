from bisect import bisect_right


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


def block_row(coordinates, target_row, want_beacons=True):
    # make an interval array for blocked intervals
    blocked = []

    # keep the beacons for the target row
    beacons = set()

    # go through the sensors and compute the manhattan distance as well as the influence on the target
    # row. Influence decreases is following: fields reserved decrease by one in both directions
    # around the position of the sensor. So our maximum influenced row has one reserved position at manhattan
    # distance.
    for sx, sy, bx, by, dist in coordinates:

        # compute distance from target row to our location
        row_distance = abs(sy - target_row)

        # add our beacon if it is in the target row
        if want_beacons and by == target_row:
            beacons.add((target_row, bx))

        # only proceed if it is smaller or equal to our manhattan distance
        if row_distance <= dist:
            # compute the amount of points to the left and the right we want to reserve
            blocked_fields = dist - row_distance

            # make the interval
            interval = [sx - blocked_fields, sx + blocked_fields]

            # append the possibly overlapping interval
            blocked.append(interval)

    # sort the intervals
    blocked.sort(key=lambda x: x[0])

    # make the merging of intervals
    merged_blocked = [blocked[0]]
    for interval in blocked[1:]:
        # check if it overlaps
        if interval[0] <= merged_blocked[-1][1] + 1:
            merged_blocked[-1][1] = max(interval[1], merged_blocked[-1][1])
        else:
            merged_blocked.append(interval)
    return merged_blocked, beacons


# from : https://gist.github.com/ericremoreynolds/2d80300dabc70eebc790
class KeyifyList(object):
    def __init__(self, inner, key):
        self.inner = inner
        self.key = key

    def __len__(self):
        return len(self.inner)

    def __getitem__(self, k):
        return self.key(self.inner[k])


def main1():
    # get the coordinates
    coordinates = read_input()

    # get the blocked intervals and the beacons
    blocked, beacons = block_row(coordinates, 2_000_000)

    # get the blocked areas
    blocked = sum(ele[1] - ele[0] + 1 for ele in blocked)

    # print the result
    print(f'The result for solution 1 is: {blocked - len(beacons)}')


def main2():

    # get the coordinates
    coordinates = read_input()

    # define the possible coordinates
    max_dist = 4_000_000

    # go through the possible rows
    for row in range(0, max_dist + 1):

        # get the blocked intervals
        blocked, _ = block_row(coordinates, row, False)

        # check that we need at least two intervals
        if len(blocked) < 2:
            continue

        # find the interval that contains the zero
        idx = bisect_right(KeyifyList(blocked, lambda x: x[1]), 0)
        idx2 = bisect_right(KeyifyList(blocked, lambda x: x[1]), max_dist)

        # check whether
        if idx2 != idx:
            print(f'The result for solution 2 is: {(blocked[idx][1]+1)*4_000_000 + row}')
            return


if __name__ == '__main__':
    main1()
    main2()
