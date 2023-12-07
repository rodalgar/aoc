# Day 7: Camel Cards
from collections import Counter
from enum import IntEnum
from typing import Callable

Hand_types = IntEnum('Hand_types',
                     {'HIGH_CARD': 1, 'ONE_PAIR': 2, 'TWO_PAIR': 3, 'THREE_OF_KIND': 4,
                      'FULL_HOUSE': 5, 'FOUR_OF_KIND': 6, 'FIVE_OF_KIND': 7})

card_strength_without_jokers = {
    'A': 13,
    'K': 12,
    'Q': 11,
    'J': 10,
    'T': 9,
    '9': 8,
    '8': 7,
    '7': 6,
    '6': 5,
    '5': 4,
    '4': 3,
    '3': 2,
    '2': 1
}

card_strength_with_jokers = {
    'A': 13,
    'K': 12,
    'Q': 11,
    'J': 0,
    'T': 9,
    '9': 8,
    '8': 7,
    '7': 6,
    '6': 5,
    '5': 4,
    '4': 3,
    '3': 2,
    '2': 1
}


def parse_input(raw_data: list[str]) -> list[tuple[str, int]]:
    return [(d[0], int(d[1]))
            for d in (tuple(line.split(' '))
                      for line in raw_data)]


# PART 1
def get_hand_type(cards: str) -> Hand_types:
    counter_cards = Counter(cards)
    counter_occurrences = Counter(counter_cards.values())
    if 5 in counter_occurrences:
        return Hand_types.FIVE_OF_KIND
    elif 4 in counter_occurrences:
        return Hand_types.FOUR_OF_KIND
    elif 3 in counter_occurrences:
        if 2 in counter_occurrences:
            return Hand_types.FULL_HOUSE
        else:
            return Hand_types.THREE_OF_KIND
    elif 2 in counter_occurrences:
        if counter_occurrences[2] == 2:
            return Hand_types.TWO_PAIR
        else:
            return Hand_types.ONE_PAIR
    else:
        return Hand_types.HIGH_CARD


# PART 2
def get_hand_type_jokers(cards: str) -> Hand_types:
    counter_cards = Counter(cards)
    n_jokers = 0
    if 'J' in counter_cards:
        n_jokers = counter_cards['J']
        del counter_cards['J']
    counter_occurrences = Counter(counter_cards.values())
    if n_jokers == 0:
        return get_hand_type(cards)
    if n_jokers == 5:
        return Hand_types.FIVE_OF_KIND
    elif n_jokers == 4:
        return Hand_types.FIVE_OF_KIND
    elif n_jokers == 3:
        if max(counter_cards.values()) == 2:
            return Hand_types.FIVE_OF_KIND
        else:
            return Hand_types.FOUR_OF_KIND
    elif n_jokers == 2:
        if max(counter_cards.values()) == 3:
            return Hand_types.FIVE_OF_KIND
        elif max(counter_cards.values()) == 2:
            return Hand_types.FOUR_OF_KIND
        else:
            return Hand_types.THREE_OF_KIND
    else:
        if max(counter_cards.values()) == 4:
            return Hand_types.FIVE_OF_KIND
        elif max(counter_cards.values()) == 3:
            return Hand_types.FOUR_OF_KIND
        elif max(counter_cards.values()) == 2:
            if counter_occurrences[2] == 2:
                return Hand_types.FULL_HOUSE
            else:
                return Hand_types.THREE_OF_KIND
        else:
            return Hand_types.ONE_PAIR


# PART 1 & 2
def calculate_winnings(data: list[tuple[str, int]], card_strength: dict[str, int],
                       get_hand_type_fun: Callable[[str], Hand_types]) -> int:
    data.sort(key=lambda x: (get_hand_type_fun(x[0]), [card_strength[x] for x in x[0]]))

    total = 0
    for rank, (_, bet) in enumerate(data, start=1):
        total += rank * bet

    return total


if __name__ == '__main__':
    with open('data/aoc2023-input-day07.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_data = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', calculate_winnings(sol_data, card_strength_without_jokers, get_hand_type))

    print('PART 2')
    print('>>>>SOLUTION: ', calculate_winnings(sol_data, card_strength_with_jokers, get_hand_type_jokers))
