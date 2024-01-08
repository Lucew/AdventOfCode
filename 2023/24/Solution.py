from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect
import z3


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append([[int(ele) for ele in info.split(",")] for info in line.split("@")])
    return inputs


def find_intersection_point(line1, line2):
    x1, y1, z1, a1, b1, c1 = line1
    x2, y2, z2, a2, b2, c2 = line2

    # Check if the lines are parallel
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None  # Lines are parallel and do not intersect

    # Solve for t1 and t2
    t1 = ((x2 - x1) * b2 - (y2 - y1) * a2) / det
    t2 = ((x2 - x1) * b1 - (y2 - y1) * a1) / det

    # collision happened in the past
    if t1 < 0 or t2 < 0:
        return None

    # Calculate the intersection point
    intersection_point = (x1 + a1 * t1, y1 + b1 * t1, z1 + c1 * t1)

    return intersection_point


def main1():
    result = 0

    # get the inputs
    lines = read_input()

    # go through the points
    for idx, ((x1, y1, z1), (vx1, vy1, vz1)) in enumerate(lines):
        for (x2, y2, z2), (vx2, vy2, vz2) in lines[idx:]:

            # check the intersection
            intersect = find_intersection_point((x1, y1, 0, vx1, vy1, 0), (x2, y2, 0, vx2, vy2, 0))
            if intersect is None:
                continue
            else:
                pass
                # print((x1, y1, z1), (x2, y2, z2), intersect)

            # check whether they meet in target area
            if all(200000000000000 <= coord <= 400000000000000 for coord in intersect[:-1]):
                result += 1

    print(f'The result for solution 1 is: {result}')


def main2():
    # BitVec is way faster than Int
    I = lambda name: z3.Int(name)

    x, y, z = I('x'), I('y'), I('z')
    vx, vy, vz = I('vx'), I('vy'), I('vz')

    s = z3.Solver()

    # get the inputs
    lines = read_input()

    for i, ((ax, ay, az), (vax, vay, vaz)) in enumerate(lines):
        t = I(f't_{i}')
        s.add(t >= 0)
        s.add(x + vx * t == ax + vax * t)
        s.add(y + vy * t == ay + vay * t)
        s.add(z + vz * t == az + vaz * t)

    assert s.check() == z3.sat

    m = s.model()
    x, y, z = m.eval(x), m.eval(y), m.eval(z)
    x, y, z = x.as_long(), y.as_long(), z.as_long()

    result = x + y + z
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
