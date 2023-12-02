# Day 2: Cube Conundrum
import operator
from dataclasses import dataclass
from functools import reduce
from typing import List, Dict


@dataclass
class Game:
    id: int
    samples: Dict[str, int]

    def set_ball_number(self, colour: str, qty: int) -> None:
        if colour not in self.samples:
            self.samples[colour] = 0
        self.samples[colour] = max(self.samples[colour], qty)


def parse_input(raw_data: List[str]):
    games = []
    for raw_game in raw_data:
        game_segments = raw_game.split(':')

        game_id = int(game_segments[0].split(' ')[1])
        g = Game(id=game_id, samples={})

        segments = game_segments[1].split(';')
        for segment in segments:
            samples = segment.strip(' ').split(',')
            for sample in samples:
                sample = sample.strip(' ').split(' ')
                g.set_ball_number(sample[1], int(sample[0]))
        games.append(g)
    return games


def filter_games(games: List[Game], rules: Dict[str, int]) -> List[Game]:
    valid_games = []
    for g in games:
        valid = True
        for color, qty in rules.items():
            valid = (color in g.samples) and (g.samples[color] <= qty)
            if not valid:
                break
        if valid:
            valid_games.append(g)
    return valid_games


sol_rules: Dict[str, int] = {
    'red': 12,
    'green': 13,
    'blue': 14
}


# PART 1
def part1(valid_games: List[Game]) -> int:
    return sum([g.id for g in valid_games])


# PART 2
def part2(all_games: List[Game]) -> int:
    return sum([reduce(operator.mul, g.samples.values()) for g in all_games])


if __name__ == '__main__':
    with open('data/aoc2023-input-day02.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_data = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', part1(filter_games(sol_data, sol_rules)))

    print('PART 2')
    print('>>>>SOLUTION: ', part2(sol_data))
