import pytest

from Main import parse_input, ending_condition_part1, ending_condition_part2, navigate_one_path, navigate_paths

test_raw_data_1 = [
    'RL',
    '',
    'AAA = (BBB, CCC)',
    'BBB = (DDD, EEE)',
    'CCC = (ZZZ, GGG)',
    'DDD = (DDD, DDD)',
    'EEE = (EEE, EEE)',
    'GGG = (GGG, GGG)',
    'ZZZ = (ZZZ, ZZZ)'
]

test_raw_data_2 = [
    'LLR',
    '',
    'AAA = (BBB, BBB)',
    'BBB = (AAA, ZZZ)',
    'ZZZ = (ZZZ, ZZZ)'
]

test_raw_data_3 = [
    'LR',
    '',
    '11A = (11B, XXX)',
    '11B = (XXX, 11Z)',
    '11Z = (11B, XXX)',
    '22A = (22B, XXX)',
    '22B = (22C, 22C)',
    '22C = (22Z, 22Z)',
    '22Z = (22B, 22B)',
    'XXX = (XXX, XXX)'
]


@pytest.mark.parametrize("raw_data, expected_directions, expected_navigation", [
    (test_raw_data_1, 'RL',
     {'AAA': ('BBB', 'CCC'), 'BBB': ('DDD', 'EEE'), 'CCC': ('ZZZ', 'GGG'), 'DDD': ('DDD', 'DDD'), 'EEE': ('EEE', 'EEE'),
      'GGG': ('GGG', 'GGG'), 'ZZZ': ('ZZZ', 'ZZZ')}),
    (test_raw_data_2, 'LLR', {'AAA': ('BBB', 'BBB'), 'BBB': ('AAA', 'ZZZ'), 'ZZZ': ('ZZZ', 'ZZZ')}),
    (test_raw_data_3, 'LR',
     {'11A': ('11B', 'XXX'), '11B': ('XXX', '11Z'), '11Z': ('11B', 'XXX'), '22A': ('22B', 'XXX'), '22B': ('22C', '22C'),
      '22C': ('22Z', '22Z'), '22Z': ('22B', '22B'), 'XXX': ('XXX', 'XXX')})])
def test_parse_input(raw_data, expected_directions, expected_navigation):
    directions, navigation = parse_input(raw_data)
    assert directions == expected_directions
    assert navigation == expected_navigation


@pytest.mark.parametrize("test_data, expected", [
    ('FOO', False),
    ('BAR', False),
    ('BAZ', False),
    ('ZZZ', True)
])
def test_ending_condition_part1(test_data, expected):
    data = ending_condition_part1(test_data)
    assert data == expected


@pytest.mark.parametrize("test_data, expected", [
    ('FOO', False),
    ('BAR', False),
    ('BAZ', True),
    ('ZZZ', True)
])
def test_ending_condition_part2(test_data, expected):
    data = ending_condition_part2(test_data)
    assert data == expected


@pytest.mark.parametrize("directions, navigation, expected", [
    ('RL',
     {'AAA': ('BBB', 'CCC'), 'BBB': ('DDD', 'EEE'), 'CCC': ('ZZZ', 'GGG'), 'DDD': ('DDD', 'DDD'), 'EEE': ('EEE', 'EEE'),
      'GGG': ('GGG', 'GGG'), 'ZZZ': ('ZZZ', 'ZZZ')}, 2),
    ('LLR', {'AAA': ('BBB', 'BBB'), 'BBB': ('AAA', 'ZZZ'), 'ZZZ': ('ZZZ', 'ZZZ')}, 6)
])
def test_navigate_one_path(directions, navigation, expected):
    data = navigate_one_path(directions, navigation, 'AAA', ending_condition_part1)
    assert data == expected


def test_navigate_paths():
    directions = 'LR'
    navigation = {'11A': ('11B', 'XXX'), '11B': ('XXX', '11Z'), '11Z': ('11B', 'XXX'), '22A': ('22B', 'XXX'),
                  '22B': ('22C', '22C'), '22C': ('22Z', '22Z'), '22Z': ('22B', '22B'), 'XXX': ('XXX', 'XXX')}
    data = navigate_paths(directions, navigation)
    assert data == 6
