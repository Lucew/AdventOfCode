def read_input(path: str = 'input.txt'):
    rows = []
    cols = []
    diags = []
    maxy = 0
    maxx = 0
    miny = 0
    minx = 0
    with open(path) as filet:
        for line in filet.readlines():

            # make a guard clause
            if len(line) < 2:
                continue

            # get start end end point
            start, end = line.split(' -> ')

            # get start end end coordintes
            x1, y1 = start.split(',')
            x2, y2 = end.split(',')
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)

            # update the maximum and minimum
            maxx = max(maxx, x1, x2)
            minx = min(minx, x1, x2)
            maxy = max(maxy, y1, y2)
            miny = min(miny, y1, y2)

            # append to the right list
            if x1 == x2:

                # sort points as we like them (from up to down)
                if y2 >= y1:
                    cols.append(((y1, x1), (y2, x2)))
                else:
                    cols.append(((y2, x2), (y1, x1)))
            elif y1 == y2:
                if x2 >= x1:
                    rows.append(((y1, x1), (y2, x2)))
                else:
                    rows.append(((y2, x2), (y1, x1)))
            else:
                if y2 >= y1:
                    diags.append(((y1, x1), (y2, x2)))
                else:
                    diags.append(((y2, x2), (y1, x1)))

    assert miny == 0 and minx == 0, 'Something is fishy.'
    return rows, cols, diags, maxx, maxy


def pretty_matrix(matrix):
    for row in matrix:
        print(row)
    print()


def count_matrix(matrix):
    counter = 0
    for row in matrix:
        for ele in row:
            counter += ele > 1
    return counter


def main1():

    # get the information
    rows, cols, diags, maxcol, maxrow = read_input()

    # make the grid
    matrix = [[0]*(maxcol+1) for _ in range(maxrow+1)]

    # go through the rows
    for (start_rx, start_cx), (end_rx, end_cx) in rows:
        row = matrix[start_rx]
        for cx in range(start_cx, end_cx+1):
            row[cx] += 1
    # pretty_matrix(matrix)

    # go through the columns
    for (start_rx, start_cx), (end_rx, end_cx) in cols:
        for rx in range(start_rx, end_rx+1):
            matrix[rx][start_cx] += 1
    # pretty_matrix(matrix)

    # go through the diagonals
    for (start_rx, start_cx), (end_rx, end_cx) in diags:
        # check the diagonal direction
        updater = 1
        if start_cx > end_cx:
            updater = -1
        for rx in range(start_rx, end_rx+1):
            matrix[rx][start_cx] += 1
            start_cx += updater
    # pretty_matrix(matrix)

    # get the count of elements
    counter = count_matrix(matrix)
    print(f'There are {counter} dangerous spots.')




if __name__ == '__main__':
    main1()