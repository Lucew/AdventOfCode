import functools
import collections
import tqdm


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            position, velocity = line.split(' v=')
            position = position[2:]
            inputs.append([[int(ele) for ele in position.split(',')], [int(ele) for ele in velocity.split(',')]])
    return inputs


def pretty_print_robots(robots, m, n):
    field = [['.']*n for _ in range(m)]
    for position, _ in robots:
        curr_element = field[position[1]][position[0]]
        field[position[1]][position[0]] = 1 if curr_element == '.' else curr_element+1
    for row in field:
        print("".join(str(ele) for ele in row))


def rearrange_robots(robots: list[list[list[int, int]]], m: int, n: int):
    for position, velocity in robots:

        # make some modulo stuff
        position[0] = (position[0] + velocity[0]) % n
        position[1] = (position[1] + velocity[1]) % m


def print_christmas_tree(m: int, n:int):
    field = []
    for rx in range(m):
        field.append([])
        row = field[-1]
        for cx in range(n):

            # check how far we are from the middle
            if (abs(cx-n//2) <= rx < (n//2+1)) or (rx == (n//2+1) and cx == n//2):
                row.append('X')
            else:
                row.append('.')
    for row in field:
        print("".join(str(ele) for ele in row))


def main1():

    m = 103  # 7
    n = 101  # 11
    seconds = 100

    # get the robots
    robots = read_input()
    # robots = robots[-2:-1]

    # get the new positions after 100 seconds
    quadrants = collections.defaultdict(list)
    for position, velocity in robots:

        # make some modulo stuff
        position[0] = (position[0]+velocity[0]*seconds) % n
        position[1] = (position[1]+velocity[1]*seconds) % m

        # check the quadrant
        px, xrest = divmod(position[0], (n//2))
        py, yrest = divmod(position[1], (m//2))
        if (px == 1 and not xrest) or (py == 1 and not yrest):
            continue
        quadrants[(px >= 1, py >= 1)].append(position)
    print(f'The result for solution 1 is: {functools.reduce(lambda x, y: x*y, map(len, quadrants.values()), 1)}')


def robot_islands(robots: list[list[list[int, int]]]):

    # translate the robot positions into dict for faster lookup
    posdict = collections.Counter(tuple(position) for position, _ in robots)

    # check for islands within the robots
    visited = set()
    largest_island = 0
    for (px, py) in posdict.keys():

        # check whether we were already here
        if (px, py) in visited:
            continue

        # start dfs to search for islands within the image
        stack = [(px, py)]
        curr_visited = posdict[(px, py)]
        while stack:

            # get current positions
            rx, cx = stack.pop()

            # go through the neighbors
            for nrx, ncx in [(rx+1, cx), (rx-1, cx), (rx, cx+1), (rx, cx-1)]:
                if (nrx, ncx) in visited or (nrx, ncx) not in posdict:
                    continue
                else:
                    stack.append((nrx, ncx))
                    curr_visited += posdict[(nrx, ncx)]
                    visited.add((nrx, ncx))

        # check for the largest island
        largest_island = max(largest_island, curr_visited)
    return largest_island


def check_robot_cycle(robots: list[list[list[int, int]]], m: int, n: int):

    # get elements that lie in the middle cross of the field
    cross_elements = {(n//2, rx): [] for rx in range(m)}
    cross_elements.update({(cx, m//2): [] for cx in range(n)})


def check_diagonal(robots: list[list[list[int, int]]], m: int, n: int):

    # translate the robot positions into dict for faster lookup
    posdict = set(tuple(position) for position, _ in robots)

    # go through the diagonal
    return all((n//2, rx) in posdict for rx in range(m)) and all((cx, m//2) in posdict for cx in range(n))


def main2(testing: bool = False):

    m = 7 if testing else 103
    n = 11 if testing else 101

    # get the input
    robots = read_input()

    # go through the seconds and check
    threshold = int(len(robots)*0.4)
    solution = None
    for seconds in tqdm.tqdm(range(100_000_000), desc='Searching Christmas'):
        rearrange_robots(robots, m, n)
        largest_island = robot_islands(robots)
        if largest_island > threshold:
            print(seconds+1, largest_island)
            pretty_print_robots(robots, m, n)
            solution = seconds+1
            break

    print(f'The result for solution 2 is: {solution}')


if __name__ == '__main__':
    main1()
    main2()
