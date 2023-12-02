import pytest

from Main import Game, parse_input, filter_games, part1, part2

test_raw_data = [
    'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
    'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
    'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
    'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
    'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'
]

test_rules = {
    'red': 12,
    'green': 13,
    'blue': 14
}


def get_test_data():
    return [Game(id=1, samples={'blue': 6, 'red': 4, 'green': 2}),
            Game(id=2, samples={'blue': 4, 'green': 3, 'red': 1}),
            Game(id=3, samples={'green': 13, 'blue': 6, 'red': 20}),
            Game(id=4, samples={'green': 3, 'red': 14, 'blue': 15}),
            Game(id=5, samples={'red': 6, 'blue': 2, 'green': 3})]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == get_test_data()


def test_filter_games():
    data = filter_games(get_test_data(), test_rules)
    assert data == [Game(id=1, samples={'blue': 6, 'red': 4, 'green': 2}),
                    Game(id=2, samples={'blue': 4, 'green': 3, 'red': 1}),
                    Game(id=5, samples={'red': 6, 'blue': 2, 'green': 3})]


def test_part1():
    data = part1([Game(id=1, samples={'blue': 6, 'red': 4, 'green': 2}),
                  Game(id=2, samples={'blue': 4, 'green': 3, 'red': 1}),
                  Game(id=5, samples={'red': 6, 'blue': 2, 'green': 3})])
    assert data == 8


def test_part2():
    data = part2(get_test_data())
    assert data == 2286
