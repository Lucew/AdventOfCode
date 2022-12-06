#!/usr/bin/env python3

def firstStart(line: str):
    line = line[:-1]
    for index in range(len(line) - 3):
        tester = line[index:index + 4]
        if max(map(lambda char: tester.count(char), tester)) == 1:
            print(index + 4)
            break


def secondStar(line: str):
    line = line[:-1]
    for index in range(len(line)-13):
        tester = line[index:index+14]
        if max(map(lambda char: tester.count(char), tester)) == 1:
            print(index+14)
            break

def main1():
    input = open("input.txt", "r")
    Lines = input.readlines()
    firstStart(Lines[0])


def main2():
    input = open("input.txt", "r")
    Lines = input.readlines()
    secondStar(Lines[0])


if __name__ == '__main__':
    main1()
    main2()
