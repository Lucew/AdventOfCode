from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


def read_input(path: str = 'input.txt'):
    algorithm = []
    image = []
    alg_finished = False
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            if not line:
                alg_finished = True
                continue
            if alg_finished:
                image.append(list(line))
            else:
                algorithm.append(line)

    # rejoin the algorithm
    algorithm = "".join(algorithm)
    print(algorithm)
    return algorithm, image


def extend_image(image, filler):

    # compute the current width
    w = len(image[0]) + 2

    # initialize a new map
    new_map = list()

    # create the first empty line
    new_map.append([filler] * w)

    # create the outside empty columns
    for line in image:
        new_map.append([filler] + line + [filler])

    # create the last empty line
    new_map.append([filler] * w)
    return new_map


def translate_field(image, rx, cx, filler):

    # go around the pixel to create the number
    result = 0
    m = len(image)
    n = len(image[0])
    for nrx, ncx in [(rx-1, cx-1), (rx-1, cx), (rx-1, cx+1), (rx, cx-1), (rx, cx), (rx, cx+1), (rx+1, cx-1), (rx+1, cx), (rx+1, cx+1)]:
        result <<= 1
        if 0 <= nrx < m and 0 <= ncx < n:
            result += image[nrx][ncx]
        else:
            result += filler
    return result


def main1():

    # get the input of the image
    algorithm, image = read_input('input.txt')

    # transform the image into numbers
    for rx, row in enumerate(image):
        for cx, ele in enumerate(row):
            image[rx][cx] = 1 if ele == '#' else 0

    # transform the algorithm into numbers
    algorithm = [1 if ele == '#' else 0 for ele in algorithm]

    # go through the turns
    for turn in range(1, 3):

        # determine state of infinite pixels
        filler = 1 if algorithm[0] == 1 and algorithm[-1] == 0 and not turn % 2 else 0

        # create the new image by extending the old one
        image = extend_image(image, filler)

        # copy the image and apply the changes
        tmp = [[0]*len(image[0]) for row in image]
        for rx, row in enumerate(image):
            for cx, ele in enumerate(row):
                tmp[rx][cx] = algorithm[translate_field(image, rx, cx, filler)]
        image = tmp

    print(f'The result for solution 1 is: {sum(ele for row in image for ele in row)}')


def main2():
    # get the input of the image
    algorithm, image = read_input('input.txt')

    # transform the image into numbers
    for rx, row in enumerate(image):
        for cx, ele in enumerate(row):
            image[rx][cx] = 1 if ele == '#' else 0

    # transform the algorithm into numbers
    algorithm = [1 if ele == '#' else 0 for ele in algorithm]

    # go through the turns
    for turn in range(1, 51):

        # determine state of infinite pixels
        filler = 1 if algorithm[0] == 1 and algorithm[-1] == 0 and not turn % 2 else 0

        # create the new image by extending the old one
        image = extend_image(image, filler)

        # copy the image and apply the changes
        tmp = [[0] * len(image[0]) for row in image]
        for rx, row in enumerate(image):
            for cx, ele in enumerate(row):
                tmp[rx][cx] = algorithm[translate_field(image, rx, cx, filler)]
        image = tmp

    print(f'The result for solution 2 is: {sum(ele for row in image for ele in row)}')


if __name__ == '__main__':
    main1()
    main2()
