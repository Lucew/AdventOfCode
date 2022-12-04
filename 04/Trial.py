def main():

    # Task 1 -----------------------------------------------------------------------------------------------------------
    print('Solution 1 -----------------------------------')
    # normal python loop
    result = 0
    start = 1
    inclusive_end = 200
    for num in range(start, inclusive_end+1):
        result += num
    print(f'The sum of the numbers from {start} to {inclusive_end} is: {result}')

    # using generator comprehension and built-in sum (faster and more pythonic)
    result = sum(num for num in range(start, inclusive_end+1))
    print(f'The sum of the numbers from {start} to {inclusive_end} is: {result}\n')

    # Task 2 -----------------------------------------------------------------------------------------------------------
    print('Solution 2 ---------------------------------------')

    # normal python loop
    result = 0
    start = 45
    inclusive_end = 199
    for num in range(start, inclusive_end + 1):
        if num % 2:
            result += num
    print(f'The sum of the odd numbers from {start} to {inclusive_end} is: {result}')

    # using generator comprehension and built-in sum (faster and more pythonic)
    result = sum(num for num in range(start, inclusive_end + 1) if num % 2)
    print(f'The sum of the odd numbers from {start} to {inclusive_end} is: {result}\n')

    # Task 2 -----------------------------------------------------------------------------------------------------------
    print('Solution 3 ---------')

    # normal python loop
    start = 1
    inclusive_end = 10
    separator = ' '
    for num in range(inclusive_end, start-1, -1):
        print(num, end=separator)
    print()

    # using string joining and generator expression with int to string conversion
    print(separator.join(str(num) for num in range(inclusive_end, start-1, -1)))


if __name__ == '__main__':
    main()
