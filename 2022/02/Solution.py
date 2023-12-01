from enum import Enum

def get_inputs(path='input.txt'):
    # a list for the inputs
    inputs = []

    with open(path) as filet:
        for line in filet.readlines():
            # check for empty line
            if len(line) > 1:
                inputs.append(line[:-1].split(' '))
    return inputs


# make an enum for the scores
class Symbols(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


# make an enum for the winning
class Outcome(Enum):
    WIN = 1
    DRAW = 2
    LOSS = 3


# make an evaluation function
def eval_game(opponent: Symbols, self: Symbols):
    score = 0
    if opponent == self:
        score = 3
    elif (opponent == Symbols.SCISSORS and self == Symbols.ROCK) \
            or (opponent == Symbols.PAPER and self == Symbols.SCISSORS) \
            or (opponent == Symbols.ROCK and self == Symbols.PAPER):
        score = 6
    return self.value + score


def main1():

    # get the games
    games = get_inputs()

    # make a translation dict
    normal = {'A': Symbols.ROCK, 'B': Symbols.PAPER, 'C': Symbols.SCISSORS}
    strategy = {'X': Symbols.ROCK, 'Y': Symbols.PAPER, 'Z': Symbols.SCISSORS}

    # go through the games and decode them
    score = 0
    for opponent, self in games:

        # translate the symbols
        opponent = normal[opponent]
        self = strategy[self]

        # get the score
        score += eval_game(opponent, self)

    # echo the result
    print(f'Result is: {score}')


def get_symbol(opponent, outcome: Outcome):
    if outcome == Outcome.DRAW:
        return opponent
    elif outcome == Outcome.WIN:
        if opponent == Symbols.SCISSORS:
            return Symbols.ROCK
        elif opponent == Symbols.PAPER:
            return Symbols.SCISSORS
        else:
            return Symbols.PAPER
    else:
        if opponent == Symbols.SCISSORS:
            return Symbols.PAPER
        elif opponent == Symbols.PAPER:
            return Symbols.ROCK
        else:
            return Symbols.SCISSORS


def main2():

    # get the games
    games = get_inputs()

    # make a translation list
    normal = {'A': Symbols.ROCK, 'B': Symbols.PAPER, 'C': Symbols.SCISSORS}
    outcomes = {'X': Outcome.LOSS, 'Y': Outcome.DRAW, 'Z': Outcome.WIN}

    # go through the games and get the
    score = 0
    for opponent, outcome in games:

        # get the opponent symbol
        opponent = normal[opponent]

        # get the outcome
        outcome = outcomes[outcome]
        # get the corresponding symbol
        self = get_symbol(opponent, outcome)

        # calculate the score
        score += eval_game(opponent, self)

    print(f'Score for the outcome strategy is: {score}')


if __name__ == '__main__':
    main1()
    main2()
