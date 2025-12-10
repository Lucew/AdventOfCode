import collections
import heapq
import functools
import bisect
from tqdm import tqdm
import math


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(tuple(int(ele) for ele in line.split(',')))
    return inputs


def main1():

    # get the coordinates
    inputs = read_input()

    # go through the coordinates in pairs
    result = max(abs(ele1[0]-ele2[0]+1)*abs(ele1[1]-ele2[1]+1) for idx, ele1 in enumerate(inputs) for ele2 in inputs[idx+1:])
    print(f'The result for solution 1 is: {result}')


def is_point_inside(rx: float, cx: float, edge_list: dict[int:list[tuple[int,int],...]]):
    result = 0
    for coordinate, edges in edge_list.items():
        if coordinate < cx: continue
        for ex, sx in edges:
            if ex <= rx < sx:
                result += 1
    # print(rx, cx, result)
    return result&1


def intersects_rect(rx_min: int, rx_max: int, cx_min: int, cx_max: int, row_edges, col_edges):

    # go through the col edges (horizontal) and check whether it intersects
    for ncx, vals in col_edges.items():
        if cx_min < ncx < cx_max:
            for srx, erx in vals:
                    if not (erx <= rx_min or srx >= rx_max):
                        return True

    # go through the row edges (vertical) and check whether it intersects
    for nrx, vals in row_edges.items():
        if rx_min < nrx < rx_max:
            for scx, ecx in vals:
                    if not (ecx <= cx_min or scx >= cx_max):
                        return True
    return False



def main2():
    result = 0

    # get the coordinates
    inputs = read_input()

    # get the edges and put them into the cols and rows
    row_edges = collections.defaultdict(list)
    col_edges = collections.defaultdict(list)
    for (rx1, cx1), (rx2, cx2) in zip(inputs,  inputs[1:] + [inputs[0]]):
        if rx1 == rx2:
            row_edges[rx1].append((min(cx1, cx2), max(cx1, cx2)))
        else:
            col_edges[cx1].append((min(rx1, rx2), max(rx1, rx2)))

    # go through each combination
    for idx, (rx1, cx1) in enumerate(inputs):
        for rx2, cx2 in inputs[idx+1:]:
            # calculate the area
            area = (abs(rx1-rx2)+1)*(abs(cx1-cx2)+1)

            # optimisation, we do not have to check rectangles that are smaller than we already have
            if area <= result:
                continue

            # order the points
            rx_min, rx_max = min(rx1, rx2), max(rx1, rx2)
            cx_min, cx_max = min(cx1, cx2), max(cx1, cx2)

            # check whether the point is inside
            if is_point_inside(rx_min+0.5, cx_min+0.5, col_edges) == 1 or rx1 == rx2 or cx1 == cx2:
                if not intersects_rect(rx_min, rx_max, cx_min, cx_max, row_edges, col_edges):
                    result = max(result, area)

    # maybe try ray casting
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
