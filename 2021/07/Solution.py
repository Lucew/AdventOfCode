
# make a function to read the board
def read_input(path: str = 'input.txt'):
    with open(path) as filet:
        line = filet.readline().split(',')
        line = [int(ele) for ele in line]
    return line


def compute_distance(array, median):
    return sum(abs(ele-median) for ele in array)


def compute_crab_distance(array, point):
    fuel = 0
    for ele in array:
        dist = abs(ele-point)
        fuel += ((dist+1)*dist)//2
    return fuel


def main1():

    # get all horizontal positions
    positions = read_input()

    # sort the positions to find median
    positions.sort()

    # get the median
    medians = positions[len(positions)//2:len(positions)//2+2]
    dist1 = compute_distance(positions, medians[0])
    dist2 = compute_distance(positions, medians[1])
    print(min(dist2, dist1))


def main2():

    # get all the positions
    positions = read_input()

    # get minimum and maximum position
    mined = min(positions)
    maxed = max(positions)

    # go through all distances
    min_fuel = float('inf')
    for posi in range(mined, maxed+1):
        min_fuel = min(compute_crab_distance(positions, posi), min_fuel)
    print(min_fuel)


if __name__ == '__main__':
    main1()
    main2()