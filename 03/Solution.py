import timeit
import inspect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


# make a function for score calculation
def score(char: str):
    if ord(char) < 97:
        return ord(char) - 38
    else:
        return ord(char) - 96


def main1():
    result = 0

    # get the rucksacks
    rucksacks = read_input()
    # split the rucksacks and make a set intersection to find the common items
    common_items = [set(rucksack[:len(rucksack)//2]).intersection(rucksack[len(rucksack)//2:]).pop()
                    for rucksack in rucksacks]

    # find the common items
    result = sum(map(score, common_items))
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # get the rucksacks
    rucksacks = read_input()

    # assert that we have groups of three
    assert len(rucksacks) % 3 == 0, 'Something is fishy.'

    # group the rucksacks into groups of three and find common item
    common_items = [set(rucksacks[idx*3]).intersection(*rucksacks[idx*3:idx*3+3]).pop()
                    for idx in range(len(rucksacks)//3)]

    # find the score
    result = sum(map(score, common_items))
    print(f'The result for solution 2 is: {result}')


def unholy_main1():
    print(sum(map(lambda char: ord(char) - 38 if ord(char) < 97 else ord(char) - 96, (set(rucksack.rstrip()[:len(rucksack)//2]).intersection(rucksack[len(rucksack)//2:]).pop() for rucksack in open('input.txt').readlines()))))


def unholy_main2():
    print(sum(map(lambda char: ord(char) - 38 if ord(char) < 97 else ord(char) - 96, (set(group[0].rstrip()).intersection(group[1].rstrip(), group[2].rstrip()).pop() for group in zip(*[iter(open('input.txt').readlines())]*3)))))

# Functions to time ----------------------------------------------------------------------------------------------------


def t_main1():
    result = 0

    # get the rucksacks
    rucksacks = read_input()
    # split the rucksacks and make a set intersection to find the common items
    common_items = [set(rucksack[:len(rucksack)//2]).intersection(rucksack[len(rucksack)//2:]).pop()
                    for rucksack in rucksacks]

    # find the common items
    result = sum(map(score, common_items))


def t_main2():
    result = 0

    # get the rucksacks
    rucksacks = read_input()

    # assert that we have groups of three
    assert len(rucksacks) % 3 == 0, 'Something is fishy.'

    # group the rucksacks into groups of three and find common item
    common_items = [set(rucksacks[idx*3]).intersection(*rucksacks[idx*3:idx*3+3]).pop()
                    for idx in range(len(rucksacks)//3)]

    # find the score
    result = sum(map(score, common_items))


def t_unholy_main1():
    sum(map(lambda char: ord(char) - 38 if ord(char) < 97 else ord(char) - 96, (set(rucksack.rstrip()[:len(rucksack)//2]).intersection(rucksack[len(rucksack)//2:]).pop() for rucksack in open('input.txt').readlines())))


def t_unholy_main2():
    sum(map(lambda char: ord(char) - 38 if ord(char) < 97 else ord(char) - 96, (set(group[0].rstrip()).intersection(group[1].rstrip(), group[2].rstrip()).pop() for group in zip(*[iter(open('input.txt').readlines())]*3))))


def time_the_functions(repetitions: int = 1000):
    main1_timed = timeit.Timer(lambda: t_main1()).timeit(repetitions)
    main2_timed = timeit.Timer(lambda: t_main2()).timeit(repetitions)
    unholy_main1_timed = timeit.Timer(lambda: t_unholy_main1()).timeit(repetitions)
    unholy_main2_timed = timeit.Timer(lambda: t_unholy_main2()).timeit(repetitions)

    print(f'The functions took: '
          f'\n\tmain1:\t\t\t{main1_timed/repetitions*1_000_000:.2f} \u03BCs per call.'
          f'\n\tmain2:\t\t\t{main2_timed/repetitions*1_000_000:.2f} \u03BCs per call.'
          f'\n\tunholy_main1:\t{unholy_main1_timed/repetitions*1_000_000:.2f} \u03BCs per call.'
          f'\n\tunholy_main2:\t{unholy_main2_timed/repetitions*1_000_000:.2f} \u03BCs per call.')


if __name__ == '__main__':
    main1()
    main2()
    unholy_main1()
    unholy_main2()
    time_the_functions()