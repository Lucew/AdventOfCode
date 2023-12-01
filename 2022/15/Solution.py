from bisect import bisect_left, bisect_right


# from : https://gist.github.com/ericremoreynolds/2d80300dabc70eebc790
class KeyifyList(object):
    def __init__(self, inner, key):
        self.inner = inner
        self.key = key

    def __len__(self):
        return len(self.inner)

    def __getitem__(self, k):
        return self.key(self.inner[k])


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


def merge_intervals(intervals, interval):
    # find the first interval we are overlapping with
    idx_left = bisect_left(KeyifyList(intervals, lambda x: x[1]+1), interval[0])

    # find the last interval we are overlapping with
    idx_right = bisect_right(KeyifyList(intervals, lambda x: x[0]), interval[1]+1)

    # check whether we overlap with anything
    if idx_left < len(intervals) and idx_left != idx_right:

        # get the new interval
        new_interval = [min(interval[0], intervals[idx_left][0]), max(interval[1], intervals[idx_right-1][1])]

        # get the new interval
        right_intervals = intervals[idx_right:]
        intervals = intervals[:idx_left]
        intervals.append(new_interval)
        intervals.extend(right_intervals)
    else:
        intervals.insert(idx_left, interval)
    return intervals


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

            # merge the intervals
            blocked = merge_intervals(blocked, interval)

    return blocked, beacons


def main1():
    # get the coordinates
    coordinates = read_input()

    # get the blocked intervals and the beacons
    blocked, beacons = block_row(coordinates, 2_000_000)

    # get the blocked areas
    blocked = sum(ele[1] - ele[0] + 1 for ele in blocked)

    # print the result
    print(f'The result for solution 1 is: {blocked - len(beacons)}')


def delete_space(coordinates, rx, min_col, max_col):

    # make the initial intervals
    intervals = [[min_col, max_col]]

    # go through each of the coordinates
    for sx, sy, bx, by, dist in coordinates:

        # compute distance from target row to our location
        row_distance = abs(sy - rx)

        # only proceed if it is smaller or equal to our manhattan distance
        if row_distance > dist:
            continue

        # compute the amount of points to the left and the right we want to block
        blocked_fields = dist - row_distance

        # make the blocked interval
        block_interval = [sx - blocked_fields, sx + blocked_fields]

        # make new intervals
        new_intervals = []

        # go through previous free space
        for interval in intervals:

            # check whether blocked interval is bigger or equal to our current interval
            if block_interval[0] <= interval[0] and block_interval[1] >= interval[1]:
                continue

            # check whether there is no intersect
            if interval[1] < block_interval[0] or interval[0] > block_interval[1]:
                new_intervals.append(interval)
                continue

            # make the two new arrays and check whether they are of positive length
            new_arrays = [[interval[0], block_interval[0]], [block_interval[1], interval[1]]]
            for start, end in new_arrays:
                if start <= end:
                    new_intervals.append([start, end])

        # replace the intervals
        intervals = new_intervals

        # make early stopping
        if len(intervals) == 0:
            break
    return intervals


def main2():

    # get the coordinates
    coordinates = read_input()

    # define the possible coordinates
    max_dist = 4_000_000

    # go through the possible rows
    for row in range(0, max_dist + 1):

        # get the blocked intervals
        free = delete_space(coordinates, row, 0, max_dist)

        # check whether we have free space
        if free:
            print(f'The result for solution 2 is: {free[0][0]*4_000_000 + row}')
            return


if __name__ == '__main__':
    main1()
    main2()
