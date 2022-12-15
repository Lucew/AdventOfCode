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

        # merge the intervals
        intervals = intervals[:idx_left] \
                    + [[min(interval[0], intervals[idx_left][0]), max(interval[1], intervals[idx_right-1][1])]] \
                    + intervals[idx_right:]
    else:
        intervals.insert(idx_left, interval)
    return intervals


def merge_intervals1(intervals, interval):
    # find the interval in our blocked intervals
    idx = bisect_right(KeyifyList(intervals, lambda x: x[0]), interval[0])

    # check whether it has overlap with the right neighbour and merge if necessary
    if 0 < idx and intervals[idx-1][1] + 1 >= interval[0]:

        # merge the intervals
        intervals[idx-1] = [intervals[idx-1][0], max(interval[1], intervals[idx-1][1])]

        # decrease the idx
        idx -= 1
    else:
        intervals.insert(idx, interval)

    # go through the next intervals to the right and merge until we can't merge anymore
    while idx < len(intervals) - 1 and intervals[idx+1][0] <= intervals[idx][1]+1:

        # merge the coming interval
        intervals[idx] = [intervals[idx][0], max(intervals[idx][1], intervals[idx+1][1])]

        # pop the coming interval
        intervals.pop(idx+1)


def block_row(coordinates, target_row):
    # make an interval array for blocked intervals
    blocked = []

    # keep the beacons for the target row
    beacons = set()

    # go through the sensors and compute the manhattan distance as well as the influence on the target
    # row. Influence decreases is following: fields reserved decrease by one in both directions
    # around the position of the sensor. So our maximum influenced row has one reserved position at manhattan
    # distance.
    for sx, sy, bx, by in coordinates:

        # compute manhattan distance
        dist = abs(sx - bx) + abs(sy - by)

        # compute distance from target row to our location
        row_distance = abs(sy - target_row)

        # add our beacon if it is in the target row
        if by == target_row:
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


def main2():
    # get the coordinates
    coordinates = read_input()

    # define the possible coordinates
    max_dist = 4_000_000

    # check for the search interval
    search_interval = [0, max_dist]

    # go through the possible rows
    for row in range(0, max_dist + 1):

        # get the blocked intervals
        blocked, _ = block_row(coordinates, row)

        # find the corresponding interval
        idx = bisect_right(KeyifyList(blocked, lambda x: x[0]), search_interval[0])

        # check whether we are included
        if 0 < idx and blocked[idx - 1][0] <= search_interval[0] and search_interval[1] <= blocked[idx - 1][1]:
            # there is no beacon possible in this row
            continue
        else:
            rx = row
            # make special conditions
            if idx == 0:
                cx = blocked[0][0] - 1
            else:
                cx = blocked[idx - 1][1] + 1

            # we found it
            print(rx, cx)
            print(f'The result for solution 2 is: {rx + cx * 4_000_000}')
            return


if __name__ == '__main__':
    main1()
    main2()
