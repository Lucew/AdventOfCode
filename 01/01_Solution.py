# this should be a simple task by iterating through the file and having number of calories for each elf
#
# It has time complexity O(N) where N is the number of lines of the input
# It has O(1) space complexity

max_calories = 0
current_calories = 0
with open('input.txt', 'r') as filet:
    for line in filet.readlines():

        # check for empty line
        if len(line) > 1:
            current_calories += int(line[:-1])
        else:
            max_calories = max(max_calories, current_calories)
            current_calories = 0

    # account for the last possible elf (which is not followed by an empty line)
    max_calories = max(max_calories, current_calories)

# give the output
print(f'The maximum calories any elf carries is: {max_calories}.')