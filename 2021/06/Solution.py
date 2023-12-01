from collections import Counter


# make a function to read the board
def read_input(path: str = 'input.txt'):
    with open(path) as filet:
        line = filet.readline().split(',')
        line = [int(ele) for ele in line]
    return line


# function to update the state
def update_state(state: list):

    # go through the counter by the days
    reborn = state[0]
    for days_left in range(8):
        state[days_left] = state[days_left+1]
    state[6] += reborn
    state[8] = reborn


def main1(days=80):

    # get the initial state
    state = read_input()

    # transform state to a counter
    counter_array = [0]*9
    for ele in state:
        counter_array[ele] += 1
    state = counter_array

    # update the state for the days
    for _ in range(days):
        update_state(state)
    print(sum(state))


if __name__ == '__main__':
    main1(80)
    main1(256)