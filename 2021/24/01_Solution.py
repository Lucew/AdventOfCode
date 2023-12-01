# we need to write an ALU with all the necessary information

def custom_mod(x, y):
    if x < 0 or y < 0:
        raise ValueError(f'{x} or {y} were smaller than zero in modulo operation.')
    return x % y


def custom_div(x, y):
    if y == 0:
        raise ValueError(f'{x} or {y} were smaller than zero in modulo operation.')
    return x // y


# make the operations
OPERATIONS = {
    'add': lambda x, y: x + y,
    'mul': lambda x, y: x * y,
    'div': custom_div,
    'mod': custom_mod,
    'eql': lambda x, y: int(x == y),
    'inp': lambda x, y: y,
 }

# go through the input and get all the operations
operations = []
input_counter = 0
with open('input.txt', 'r') as filet:

    # go through the lines one by one
    for line in filet.readlines():

        # check it is more than a newline
        if len(line) > 1:

            # split the line (leaving the new line character)
            line = line[:-1].split(' ')

            # check second element for beeing and int
            try:
                line[2] = int(line[2])
            except (IndexError, ValueError):
                pass

            # append to the operations
            operations.append(line)

# go through the operations and count the amount of inputs
counter = sum(operation[0] == 'inp' for operation in operations)
print(f'We found {counter} input operations.')

# split the operations into input parts
splitted_operations = []
for operation in operations:
    if operation[0] == 'inp':
        splitted_operations.append([])
    splitted_operations[-1].append(operation)

# check whether we overwrite w all the time -> w does not get used from the previous block
for idx, partial in enumerate(splitted_operations):
    if partial[0][0] != 'inp':
        raise ValueError('Something is wrong.')
    if partial[0][1] != 'w':
        print(f'Damn we overwrite anything else than w with the input.')
print()

# go through the operation blocks and check whether x will be used anywhere from the previous block
for idx, partial in enumerate(splitted_operations):
    used = False
    for operation in partial[1:]:
        if operation == ['mul', 'x', 0]:
            break
        if operation[2] == 'x':
            used = True

    # check the not used thing
    if used:
        print(f'Damn we use z in after number {idx}.')
print()

# go through the operation blocks and check whether x will be used anywhere from the previous block
for idx, partial in enumerate(splitted_operations):
    used = False
    for operation in partial[1:]:
        if operation == ['mul', 'y', 0]:
            break
        if operation[2] == 'y':
            used = True

    # check the not used thing
    if used:
        print(f'Damn we use z in after number {idx}.')
print()

# go through the operation blocks and check whether z will be used anywhere from the previous block
for idx, partial in enumerate(splitted_operations):
    used = False
    for operation in partial[1:]:
        if operation == ['mul', 'z', 0]:
            break
        if operation[2] == 'z':
            used = True

    # check the not used thing
    if used:
        print(f'Damn we use z in after number {idx}.')
print()

# go through the splitted operations and take a look if w gets overwritten anywhere
for idx, partial in enumerate(splitted_operations):
    overwritten = False
    for operation in partial[1:]:
        if operation[1] == 'w':
            overwritten = True

    # check the not used thing
    if overwritten:
        print(f'Damn we overwrite w after number {idx}.')
print()

# go through the instructions and check for differences
for idx, operations in enumerate(splitted_operations[:-1], 1):
    # check for differences per line
    cols = []
    for cx, (operation1, operation2) in enumerate(zip(operations, splitted_operations[idx])):
        if operation1 != operation2:
            cols.append(cx)
    print(cols)

# now go through the solutions recursively
result = [0]*14
print(splitted_operations[-1])


def recursive_approach(input_pointer, z, w):

    # check other stuff
    if input_pointer == 14:
        if z == 0:
            return True
        else:
            return False

    # initialize the arrays
    registers = {'x': 0, 'y': 0, 'z': z, 'w': w}

    # go through the instructions and immediately return if we have a value error
    if input_pointer >= 0:
        try:
            for operation in splitted_operations[input_pointer][1:]:
                x = registers[operation[1]]
                y = registers.get(operation[2], operation[2])
                registers[operation[1]] = OPERATIONS[operation[0]](x, y)
        except ValueError as e:
            print(e)
            return False

    # try out other possibilities going from here
    for next_number in range(9, 0, -1):
        if recursive_approach(input_pointer+1, registers['z'], next_number):
            result[input_pointer] = next_number
            return True

    return False


# recursive_approach(-1, 0, 0)
print(splitted_operations[-1])
