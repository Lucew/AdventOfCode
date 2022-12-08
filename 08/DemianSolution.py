import math


def readMatrix(lines) -> list[list[int]]:
    return list(map(lambda line: list(map(int, line.rstrip())), lines))


def removeHidden(matrix: list[list[int]]) -> list[list[int]]:
    newMat = [[-1] * len(line) for line in matrix]
    for x in range(len(matrix)):
        prev1 = -1
        prev2 = -1
        prev3 = -1
        prev4 = -1
        line1 = matrix[x]
        line2 = line1[::-1]
        line3 = [line[x] for line in matrix]
        line4 = line3[::-1]
        for y in range(len(line1)):
            if line1[y] > prev1:
                newMat[x][y] = line1[y]
                prev1 = line1[y]
            if line2[y] > prev2:
                newMat[x][-y - 1] = line2[y]
                prev2 = line2[y]
            if line3[y] > prev3:
                newMat[y][x] = line3[y]
                prev3 = line3[y]
            if line4[y] > prev4:
                newMat[-y - 1][x] = line4[y]
                prev4 = line4[y]
    return newMat


def main1():
    input = open("input.txt", "r")
    Lines = input.readlines()
    matrix = readMatrix(Lines)
    visible = removeHidden(matrix)
    print(len(visible)**2 - sum(map(lambda line: line.count(-1), visible)))


def second(matrix: list[list[int]]):
    map0 = [list(map(lambda x: x < 0, line)) for line in matrix]
    map1 = [list(map(lambda x: x < 1, line)) for line in matrix]
    map2 = [list(map(lambda x: x < 2, line)) for line in matrix]
    map3 = [list(map(lambda x: x < 3, line)) for line in matrix]
    map4 = [list(map(lambda x: x < 4, line)) for line in matrix]
    map5 = [list(map(lambda x: x < 5, line)) for line in matrix]
    map6 = [list(map(lambda x: x < 6, line)) for line in matrix]
    map7 = [list(map(lambda x: x < 7, line)) for line in matrix]
    map8 = [list(map(lambda x: x < 8, line)) for line in matrix]
    map9 = [list(map(lambda x: x < 9, line)) for line in matrix]
    maps = [map0, map1, map2, map3, map4, map5, map6, map7, map8, map9]
    maximum = 0
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            mymap = maps[matrix[x][y]]
            x1view = mymap[x][y+1:]
            x2view = (mymap[x][:y])[::-1]
            yline = [line[y] for line in mymap]
            y1view = yline[x+1:]
            y2view = (yline[:x])[::-1]
            views = [x1view, x2view, y1view, y2view]
            viewlengths = list(map(
                lambda view: view.index(
                    False)+1 if False in view else len(view),
                views))
            viewlength = math.prod(viewlengths)
            if viewlength > maximum:
                maximum = viewlength
    print(maximum)


def main2():
    input = open("input.txt", "r")
    Lines = input.readlines()
    matrix = readMatrix(Lines)
    second(matrix)


if __name__ == '__main__':
    main1()
    main2()
