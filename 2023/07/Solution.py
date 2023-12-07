import collections
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def high_level_strengths(hand: str, task_number: int = 1) -> int:
    """
    Function to compute the high level strength of a deck.

    Parameters
    ----------
    hand: The hand of cards as a string
    task_number: for which of the two solution parts this function applies

    Returns
    -------
    strength: the strength of the hand as an int
    """

    # get the cards
    cn = collections.Counter(hand)

    # check whether we have joker
    if cn["J"] and task_number == 2:

        # check whether we only have jokers
        if len(cn) == 1:
            cn["A"] = cn["J"]

        else:
            # sort the cards by frequency and value
            cards = cn.most_common(2)

            # check whether the jokers are the highest
            if cards[0][0] == "J":
                cn[cards[1][0]] += cn["J"]
            else:
                cn[cards[0][0]] += cn["J"]

        # delete the jokers
        del cn["J"]

    if len(cn) == 5:  # all different
        return 0
    elif len(cn) == 4:  # one pair somewhere
        return 1
    elif len(cn) == 3 and max(cn.values()) == 2:  # two pairs
        return 2
    elif len(cn) == 3 and max(cn.values()) == 3:  # three of a kind
        return 3
    elif len(cn) == 2 and max(cn.values()) == 3:  # full house
        return 4
    elif len(cn) == 2 and max(cn.values()) == 4:  # four of a kind
        return 5
    else:  # all equal
        return 6


def get_card_strength(cards: str, task_number: int = 1):
    if task_number == 1:
        strengths = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    elif task_number == 2:
        strengths = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    else:
        raise ValueError(f"Task number: {task_number} not supported (1 or 2).")
    strength_dict = {ele: idx for idx, ele in enumerate(reversed(strengths))}
    result = []
    for card in cards:
        result.append(strength_dict[card])
    return tuple(result)


def main1():

    # get the card decks and their corresponding value and bid
    cards = [(high_level_strengths(hand.split(" ")[0]), get_card_strength(hand.split(" ")[0]), int(hand.split(" ")[1]), )
             for hand in read_input()]
    cards.sort()
    print(f'The result for solution 1 is: {sum(idx*hand[2] for idx, hand in enumerate(cards, 1))}')


def main2():
    # get the card decks and their corresponding value and bid
    cards = [(high_level_strengths(hand.split(" ")[0], 2), get_card_strength(hand.split(" ")[0], 2),
              int(hand.split(" ")[1]))
             for hand in read_input()]
    cards.sort()
    print(f'The result for solution 2 is: {sum(idx * hand[2] for idx, hand in enumerate(cards, 1))}')


if __name__ == '__main__':
    main1()
    main2()
