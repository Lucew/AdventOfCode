#!/usr/bin/env python3


from typing import Tuple
import ast


def main1():
    input = open("input.txt", "r")
    Lines = input.readlines()
    parsed = parser(Lines)
    first(parsed)


def main2():
    input = open("input.txt", "r")
    Lines = input.readlines()
    parsed = parser(Lines)
    second(parsed)


def parser(lines: list[str]):
    pairs = []
    old = []
    oldExists = False
    for line in lines:
        if len(line) < 2:
            continue
        my = ast.literal_eval(line)
        if (oldExists):
            pairs.append(tuple([old, my]))
            oldExists = False
        else:
            old = my
            oldExists = True
    return pairs


def compare(tup: Tuple[list]):
    (first, second) = tup
    # print(tup)
    if len(first) == 0 and len(second) == 0:
        return 0
    if len(first) == 0:
        return 1
    if len(second) == 0:
        return -1
    if (isinstance(first[0], int) and isinstance(second[0], int)):
        if first[0] == second[0]:
            return compare((first[1:], second[1:]))
        elif first[0] < second[0]:
            return 1
        else:
            return -1
    if isinstance(first[0], int):
        returner = compare(([first[0]], second[0]))
        if returner == 0:
            return compare((first[1:], second[1:]))
        else:
            return returner
    if isinstance(second[0], int):
        returner = compare((first[0], [second[0]]))
        if returner == 0:
            return compare((first[1:], second[1:]))
        else:
            return returner
    else:
        returner = compare((first[0], second[0]))
        if returner == 0:
            return compare((first[1:], second[1:]))
        else:
            return returner


def first(parsed):
    total = 0
    for pos, elem in enumerate(list(map(compare, parsed))):
        if (elem == 1):
            total += pos+1
        elif elem == 0:
            print(pos)
    print(total)


def second(parsed):
    liste = [y for tup in parsed for y in tup]
    liste.append([[2]])
    liste.append([[6]])
    switched = True
    while switched:
        switched = False
        for pos in range(len(liste)-1):
            comp = compare((liste[pos], liste[pos+1]))
            if (comp == -1):
                temp = liste[pos]
                liste[pos] = liste[pos+1]
                liste[pos+1] = temp
                switched = True
            if comp == 0:
                print("ERROR")
    print((liste.index([[2]])+1) * (liste.index([[6]])+1))


if __name__ == '__main__':
    main1()
    main2()