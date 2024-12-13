import re
import math


def read_input(path: str = 'input.txt'):
    inputs = [[]]
    with open(path) as filet:
        for idx, line in enumerate(filet.readlines()):

            # strip the line
            line = line.strip()

            # check whether we have an empty line
            if not line.strip():
                inputs.append([])
            else:
                # get the numbers from the lines
                line = line.split(": ", 1)[1]

                # check which type of line we have
                inputs[-1].append(list(int(ele) for ele in re.findall("\d+", line)))
    return inputs


def solve(button_a, button_b, target):

    # copy the target
    target = target[:]

    # get the gcds for both coordinates and get them out of the equation
    gcd0 = math.gcd(button_a[0], button_b[0])
    gcd1 = math.gcd(button_a[1], button_b[1])

    # reduce the target and check whether integer solution is still possible
    target[0], rest0 = divmod(target[0], gcd0)
    target[1], rest1 = divmod(target[1], gcd1)
    if rest0 or rest1:
        return float('inf')
    button_a = [button_a[0]//gcd0, button_a[1]//gcd1]
    button_b = [button_b[0]//gcd0, button_b[1]//gcd1]

    # go through button_a first
    max_a_times = min(target[idx]//button_a[idx] for idx in range(len(target)))
    minimum_cost = float('inf')
    for a_presses in range(max_a_times+1):

        # check whether we can reach with button b
        button_b_0_presses, rest_0 = divmod(target[0], button_b[0])
        button_b_1_presses, rest_1 = divmod(target[1], button_b[1])

        # make the check
        if button_b_0_presses == button_b_1_presses and rest_0 == rest_1 and not rest_0:
            minimum_cost = min(minimum_cost, button_b_0_presses+a_presses*3)

        # update the target
        target = (target[0]-button_a[0], target[1]-button_a[1])
    return minimum_cost


def solve2(button_a, button_b, target):

    # solve the system of equations
    y, rs = divmod((button_a[0]*target[1]-button_a[1]*target[0]), (button_b[1]*button_a[0]-button_a[1]*button_b[0]))
    if rs:
        return float('inf')
    x, rs = divmod(target[0]-y*button_b[0], button_a[0])
    if rs:
        return float('inf')
    return y+x*3


def main1():
    result = 0

    # get the inputs
    machines = read_input()

    # go through the machines and make a dijkstra
    for button_a, button_b, target in machines:
        price = solve2(button_a, button_b, target)
        if price != float('inf'):
            result += price

    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # get the inputs
    machines = read_input()

    # go through the machines and make a dijkstra
    for button_a, button_b, target in machines:
        price = solve2(button_a, button_b, [target[0]+10000000000000, target[1]+10000000000000])
        if price != float('inf'):
            result += price

    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
