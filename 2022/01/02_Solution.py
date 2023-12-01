# second solution requires to find the topK elfes and sum them. We use as min heap to solve this
#
# It has time complexity O(N*logK) where N is the number of lines of the input
# It has O(1) space complexity
from heapq import heappush, heappop

max_calories = 0
max_k_calories = []
current_calories = 0
number_of_elves = 3


def update_stack(stack: list, element, k=3):
    heappush(stack, element)
    while len(stack) > k:
        heappop(stack)


with open('01_input.txt', 'r') as filet:
    for line in filet.readlines():

        # check for empty line
        if len(line) > 1:
            current_calories += int(line[:-1])
        else:
            update_stack(max_k_calories, current_calories, number_of_elves)
            current_calories = 0

    # account for the last possible elf (which is not followed by an empty line)
    update_stack(max_k_calories, current_calories)

# give the output
print(f'The maximum calories of {[number_of_elves]} elves is: {sum(max_k_calories)}.')