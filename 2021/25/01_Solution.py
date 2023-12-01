# read the input

matrix = []
with open('input.txt', 'r') as filet:
    for line in filet.readlines():
        if len(line) > 1:
            matrix.append(list(line[:-1]))


def print_matrix(print_matrix: list[list[str]]):
    print("\n".join("".join(rowed) for rowed in print_matrix))


# go through the input and check whether we can move the element given the location
counter = 0
moved = True
m = len(matrix)
n = len(matrix[0])
while moved:
    moved = False
    counter += 1

    # make the east moving things first
    for rx, row in enumerate(matrix):

        # check whether the last one will switch over
        switch_over = False
        if row[-1] == '>' and row[0] == '.':
            moved = True
            switch_over = True

        current = row[0]
        for cx in range(n-1):
            if current == '>' and row[cx+1] == '.':
                current = row[cx+1]
                row[cx] = '.'
                row[cx+1] = '>'
                moved = True
            else:
                current = row[cx+1]

        # make the last east facing thing
        if switch_over:
            row[0] = '>'
            row[-1] = '.'

    # print_matrix(matrix)
    # print('asdasdasdasdasdasdasdasdasd')

    # make the south going things second
    for cx in range(n):

        # check whether the last ones will roll over
        switch_over = False
        if matrix[-1][cx] == 'v' and matrix[0][cx] == '.':
            moved = True
            switch_over = True

        # save the current element and go over the table
        current = matrix[0][cx]
        for rx in range(m-1):
            if current == 'v' and matrix[rx+1][cx] == '.':
                current = matrix[rx+1][cx]
                matrix[rx][cx] = '.'
                matrix[rx+1][cx] = 'v'
                moved = True
            else:
                current = matrix[rx + 1][cx]

        if switch_over:
            matrix[0][cx] = 'v'
            matrix[-1][cx] = '.'

    # print_matrix(matrix)
    # print()
print(counter)
