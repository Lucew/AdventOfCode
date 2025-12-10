import collections
import heapq
import functools
import bisect
import sys
import random
import math
sys.setrecursionlimit(5000)

def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line.split(' '))
    return inputs


def is_correct(state: tuple[int,...], pattern: str) -> bool:
    return all(pattern[idx+1] == '#' if number&1 else pattern[idx+1] == '.' for idx, number in enumerate(state))

def update_state(state: tuple[int,...], button: set[int]) -> tuple[int,...]:
    new_state = tuple((ele+1)&1 if idx in button else ele for idx, ele in enumerate(state))
    return new_state


def press_buttons(state: tuple[int,...], button_presses: int, button_pressed: int, buttons: list[set[int]], pattern: str, cache: dict[tuple[int]:int]) -> int:

    # check whether we have encountered this state
    if state in cache:
        return cache[state]

    # check whether we pressed too many buttons
    if button_presses >= cache[(-1,)]:
        return 10_000_000_000

    # check whether we are finished
    if is_correct(state, pattern):
        cache[state] = 0
        cache[(-1,)] = button_presses
        return 0

    # try different button presses
    cache[state] = 10_000_000_000
    min_presses = min(press_buttons(update_state(state, button), button_presses+1, btx, buttons, pattern, cache)+1 for btx, button in enumerate(buttons) if btx != button_pressed)
    cache[state] = min_presses
    return min_presses


def main1():
    result = 0

    # get the inputs
    inputs = read_input()

    # go through the machines
    for machine in inputs:

        # get the list of button presses
        buttons = [{int(ele) for ele in button[1:-1].split(',')} for button in machine[1:-1]]

        # get the pattern
        pattern = machine[0]

        # make the cache
        cache = dict()
        cache[(-1,)] = float('inf')

        # check the button presses
        result += press_buttons(tuple(0 for _ in pattern[1:-1]), 0, -1, buttons, pattern, cache)

    # get the s
    print(f'The result for solution 1 is: {result}')


def joltage_correct(state: tuple[int,...], pattern: tuple[int,...]) -> bool:
    return state == pattern

def update_joltage(state: tuple[int,...], button: set[int]) -> tuple[int,...]:
    new_state = tuple(ele+1 if idx in button else ele for idx, ele in enumerate(state))
    return new_state

def joltage_valid(state: tuple[int,...], pattern: tuple[int,...]) -> bool:
    return all(target >= number for number, target in zip(state, pattern))


def min_presses(buttons, b):
    # buttons: list of masks or index lists
    start = tuple(b)
    goal = (0,) * len(b)

    max_size = max(len(btn) for btn in buttons)

    def h(rem):
        s = sum(rem)
        if s == 0: return 0
        h1 = max(rem)
        h2 = (s + max_size - 1) // max_size
        return max(h1, h2)

    pq = [(h(start), 0, start)]
    best_g = {start: 0}

    while pq:
        f, g, rem = heapq.heappop(pq)
        if rem == goal:
            return g

        if g != best_g.get(rem):
            continue

        # Expand
        for btn in buttons:
            # Only press if all affected rem[i] > 0
            if any(rem[i] == 0 for i in btn):
                continue
            new = list(rem)
            for i in btn:
                new[i] -= 1
            new = tuple(new)

            ng = g + 1
            if ng < best_g.get(new, 10**18):
                best_g[new] = ng
                heapq.heappush(pq, (ng + h(new), ng, new))

    return None  # impossible



def main2():
    result = 0

    # get the inputs
    inputs = read_input()

    # go through the machines
    for machine in inputs:
        # get the list of button presses
        buttons = [{int(ele) for ele in button[1:-1].split(',')} for button in machine[1:-1]]
        pattern = list(int(ele) for ele in machine[-1][1:-1].split(','))

        # reduce the solutions space by checking whether there is one state only accessible by a single button
        overlap = [[] for _ in pattern]
        for bdx, button in enumerate(buttons):
            for idx in button:
                overlap[idx].append(bdx)
        print([len(ele) for ele in overlap])
        continue

        # go through the pattern digits and check whether there is only a single button that accesses the current digit
        for pdx, button_idces in enumerate(overlap):
            if len(button_idces) == 1:
                result += pattern[pdx]
                for bdx in buttons[button_idces[0]]:
                    pattern[bdx] -= pattern[pdx]
        pattern = tuple(pattern)

        # try dfs approach
        stack = [(tuple(0 for _ in pattern), 0)]
        psum = sum(pattern)
        curr_result = psum
        visited = {stack[0][0]: 0}
        while stack:

            # get the current element
            state, steps = stack.pop()

            # check whether the state is divisible by the current
            if all(num != 0 and target % num == 0 for num, target in zip(state, pattern)):
                print("Found one!")
                curr_result = pattern[0]//state[0]*steps

            # check whether state is valid
            if steps >= curr_result:
                continue

            # check how many reductions we have minimally left
            if steps + max(pattern) >= psum:
                continue

            # go through the buttons
            for button in sorted(buttons, key=lambda x: sum(len(overlap[btx]) for btx in x)):
                new_state = update_joltage(state, button)
                if steps+1 >= visited.get(new_state, psum):
                    continue
                if not joltage_valid(new_state, pattern):
                    continue
                if steps+1 >= curr_result:
                    continue
                if joltage_correct(new_state, pattern):
                    print("Found correct!")
                    curr_result = steps+1
                    continue
                visited[new_state] = steps+1
                stack.append((new_state, steps+1))
        result += curr_result
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
