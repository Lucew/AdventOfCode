import functools
import collections


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            line = tuple(int(ele) for ele in line.split(','))
            inputs.append(line)
    return inputs


def main1():
    # get the input
    inputs = read_input()

    # convert to a set for fast lookup
    inputs = set(inputs)

    # go through cubes and add six (number of sides) minus the amount fo immediate neighbours
    result = 0
    for (x, y, z) in inputs:
        result += 6
        for nx, ny, nz in [(x+1, y, z), (x-1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z-1)]:
            if (nx, ny, nz) in inputs:
                result -= 1
    print(f'The result for solution 1 is: {result}')


def create_cubicle(dimensions, idx=0):
    result = []
    if idx < len(dimensions) - 1:
        for _ in range(dimensions[idx][1] - dimensions[idx][0] + 1):
            result.append(create_cubicle(dimensions, idx+1))
    else:
        result = [0]*(dimensions[idx][1] - dimensions[idx][0] + 1)
    return result


def bfs(x, y, z, cubicle):

    # make a safety precaution
    if cubicle[x][y][z] == -1:
        return 0
    elif cubicle[x][y][z] == 1:
        return 1

    # put in the starting cubicle
    queue = collections.deque([(x, y, z)])

    # mark cubicle as visited
    cubicle[x][y][z] = -1

    # go through the queue of 3D coordinates (cubicles) we need to look at
    result = 0
    while queue:

        # pop a cubicle
        x, y, z = queue.popleft()

        # go through the neighbours on each side and count occupied neighbours (==1)
        # append not touched, empty neighbours (==0) to the queue
        # mark this cubicle as visited
        for nx, ny, nz in [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]:

            # check whether we out of scope
            if nx < 0 or nx >= len(cubicle) or ny < 0 or ny >= len(cubicle[0]) or nz < 0 or nz >= len(cubicle[0][0]):
                continue

            # check the cubicle type
            if cubicle[nx][ny][nz] == 1:

                # count a side
                result += 1

            elif cubicle[nx][ny][nz] == 0:

                # append cubicle to queue
                queue.append((nx, ny, nz))

                # mark cubicle as visited
                cubicle[nx][ny][nz] = -1
    return result


def main2(max_elements=1_000_000):

    # get the inputs
    inputs = read_input()

    # convert to a set for fast lookup
    inputs = set(inputs)

    # get the maximum and minimum of each coordinate
    dimensions = [[float('inf'), float('-inf')] for _ in range(3)]
    for ele in inputs:
        for idx, dim in enumerate(dimensions):
            dim[0] = min(dim[0], ele[idx])
            dim[1] = max(dim[1], ele[idx])

    # calculate the amount of elements if we would create n-dimensional matrix
    element_number = functools.reduce(lambda d1, d2: d1*(d2[1] - d2[0]), dimensions, 1)
    assert element_number < max_elements, 'Cubicle will get too big.'

    # create 3D matrix to do dfs for holes
    cubicle = create_cubicle(dimensions)

    # place the values
    for (x, y, z) in inputs:
        cubicle[x-dimensions[0][0]][y-dimensions[1][0]][z-dimensions[1][0]] = 1
    result = 0

    # go through the outer layers of each dimension and make a bfs (marking visited elements with -1 to not visit
    # again). Then count the amount of rocks we touch
    for x in range(len(cubicle)):
        for y in range(len(cubicle[0])):
            result += bfs(x, y, 0, cubicle)
            result += bfs(x, y, len(cubicle[0][0])-1, cubicle)
    for y in range(len(cubicle[0])):
        for z in range(len(cubicle[0][0])):
            result += bfs(0, y, z, cubicle)
            result += bfs(len(cubicle)-1, y, z, cubicle)
    for x in range(len(cubicle)):
        for z in range(len(cubicle[0][0])):
            result += bfs(x, 0, z, cubicle)
            result += bfs(x, len(cubicle[0])-1, z, cubicle)
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
