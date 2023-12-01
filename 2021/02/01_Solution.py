
# read the file
forward = 0
depth = 0
with open('input.txt') as filet:
    for line in filet.readlines():
        # split the line
        line = line.split(' ')
        if len(line) > 1:

            # make the operation
            if line[0] == 'forward':
                forward += int(line[1])
            elif line[0] == 'down':
                depth += int(line[1])
            elif line[0] == 'up':
                depth -= int(line[1])
                depth = max(depth, 0)
            else:
                raise NotImplementedError
print(forward*depth)

# second solution
forward = 0
depth = 0
aim = 0
with open('input.txt') as filet:
    for line in filet.readlines():
        # split the line
        line = line.split(' ')
        if len(line) > 1:

            # get the number
            number = int(line[1])

            # make the operation
            if line[0] == 'forward':
                forward += number
                depth += aim*number
                depth = max(0, depth)
            elif line[0] == 'down':
                aim += number
            elif line[0] == 'up':
                aim -= number
            else:
                raise NotImplementedError
print(forward*depth)