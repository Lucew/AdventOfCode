def main1():
    # read the input into a matrix
    matrix = []
    with open('input.txt') as filet:
        for line in filet.readlines():
            if len(line) > 1:
                matrix.append(line[:-1])

    # count the most common bit for each number
    gamma = 0
    epsilon = 0
    for cx in range(len(matrix[0])):

        ones = 0
        for rx in range(len(matrix)):
            ones += matrix[rx][cx] == '1'

        # get the most common element
        most_common = 1 if ones > len(matrix) // 2 else 0

        # update the numbers
        gamma = (gamma << 1) + most_common
        epsilon = (epsilon << 1) + (1-most_common)
    print(gamma, epsilon, epsilon*gamma)


# Solution 2 -----------------------------------------------------------------------------------------------------------

# make a function to find the amount of rows left and the amount of ones in this column
def find_ones(matrix, column, row_set):
    ones_amount = 0
    for rx in row_set:
        ones_amount += matrix[rx][column] == '1'

    return ones_amount, len(row_set)


def main2():

    # read the input into a matrix
    matrix = []
    with open('input.txt') as filet:
        for line in filet.readlines():
            if len(line) > 1:
                matrix.append(line[:-1])

    # create a set of rows
    rows = set(rx for rx in range(len(matrix)))

    # find the oxygen number first
    for cx in range(len(matrix[0])):

        # find the number of ones and number of rows left
        ones, rows_left = find_ones(matrix, cx, rows)

        # check whether we have only one row left
        if rows_left == 1:
            break

        # find the most common number
        most_common = '1'
        if ones < rows_left //2 or (ones == rows_left//2 and rows_left % 2):
            most_common = '0'

        # go through the rows and delete numbers
        for rx in range(len(matrix)):
            if rx in rows and matrix[rx][cx] != most_common:
                rows.remove(rx)

    oxygen_rating = int(matrix[list(rows)[0]], 2)
    print(f'Oxygen rating is: {oxygen_rating}')

    # create a set of rows
    rows = set(rx for rx in range(len(matrix)))

    # find the scrubber rating
    for cx in range(len(matrix[0])):

        # find the number of ones and number of rows left
        ones, rows_left = find_ones(matrix, cx, rows)

        # check whether we have only one row left
        if rows_left == 1:
            break

        # find the most common number
        most_common = '0'
        if ones < rows_left // 2 or (ones == rows_left // 2 and rows_left % 2):
            most_common = '1'

        # go through the rows and delete numbers
        for rx in range(len(matrix)):
            if rx in rows and matrix[rx][cx] != most_common:
                rows.remove(rx)

    scrubber_rating = int(matrix[list(rows)[0]], 2)
    print(f'Scrubber rating is: {scrubber_rating}')

    # get the final result
    print(f'Final result is: {scrubber_rating*oxygen_rating}')
main2()

# make a function to delete rows we do not use anymore

