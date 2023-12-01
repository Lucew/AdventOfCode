with open('input.txt') as filet:
    prev_depth = -500
    counter = -1
    for line in filet.readlines():
        if len(line) > 1:
            curr_depth = int(line[:-1])
            if curr_depth > prev_depth:
                counter += 1
            prev_depth = curr_depth
print(counter)


depth = []
with open('input.txt') as filet:
    for line in filet.readlines():
        if len(line) > 1:
            depth.append(int(line[:-1]))

# make a sliding window
prev_sum = sum(depth[:3])
counter = 0
for idx in range(1, len(depth)-2):
    new_sum = prev_sum + depth[idx+2] - depth[idx-1]
    if new_sum > prev_sum:
        counter += 1
    prev_sum = new_sum
print(counter)