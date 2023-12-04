# Day 4: Scratchcards
import operator
from functools import reduce

Card = tuple[int, list[int], list[int]]


def parse_input(raw_data: list[str]) -> list[Card]:
    def parse_series(raw_series: str) -> list[int]:
        raw_series = raw_series.strip()
        return list(map(int, filter(lambda x: x if x != '' else None, raw_series.split(' '))))

    parsed_lines = []
    for line in raw_data:
        card_contents = line.split(':')
        id_card = int(list(filter(lambda x: x if x != '' else None, card_contents[0].split(' ')))[1])
        number_series = card_contents[1].split('|')
        winning_numbers = parse_series(number_series[0])
        my_numbers = parse_series(number_series[1])
        parsed_lines.append((id_card, winning_numbers, my_numbers))

    return parsed_lines


def calculate_matches(card: Card) -> int:
    set_winning = set(card[1])
    set_my_numbers = set(card[2])

    matches = set_my_numbers.intersection(set_winning)
    return len(matches)


def calculate_points(card: Card) -> int:
    n_matches = calculate_matches(card)
    return 2 ** (n_matches - 1) if n_matches > 0 else 0


def part1(cards: list[Card]) -> int:
    return reduce(operator.add, map(calculate_points, cards))


def part2(cards: list[Card]) -> int:
    card_instances = {i + 1: 1 for i in range(len(cards))}

    for ix, card in enumerate(cards, start=1):
        n_matches = calculate_matches(card)
        if n_matches > 0:
            self_occurrence = card_instances[ix]
            for i in range(n_matches):
                card_instances[ix + i + 1] += self_occurrence

    return sum(card_instances.values())


if __name__ == '__main__':
    with open('data/aoc2023-input-day04.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

        sol_data = parse_input(sol_raw_data)

        print('PART 1')
        print('>>>>SOLUTION: ', part1(sol_data))

        print('PART 2')
        print('>>>>SOLUTION: ', part2(sol_data))
