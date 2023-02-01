import pytest
from Main import parse_input, map_opponent_actions, get_own_action_part1, wins_against, get_round_outcome, \
    get_own_action_part2, do_match

test_raw_data = [
    'A Y',
    'B X',
    'C Z'
]


def get_test_data_p1():
    return ['R P', 'P R', 'S S']


def get_test_data_p2():
    return ['R R', 'P R', 'S R']


@pytest.mark.parametrize("test_data, test_opponent_actions, own_action_fun, expected", [
    (['A Z'], map_opponent_actions, get_own_action_part1, ['R S']),
    (test_raw_data, map_opponent_actions, get_own_action_part1, get_test_data_p1()),
    (test_raw_data, map_opponent_actions, get_own_action_part2, get_test_data_p2())
])
def test_parse_input(test_data, test_opponent_actions, own_action_fun, expected):
    data = parse_input(test_data, test_opponent_actions, own_action_fun)
    assert data == expected


@pytest.mark.parametrize("step, expected", [
    ('R R', 'T'),
    ('R P', 'W'),
    ('R S', 'L'),
    ('P R', 'L'),
    ('P P', 'T'),
    ('P S', 'W'),
    ('S R', 'W'),
    ('S P', 'L'),
    ('S S', 'T')
])
def test_get_round_outcome(step, expected):
    data = get_round_outcome(step, wins_against)
    assert data == expected


@pytest.mark.parametrize("steps, expected", [
    ([get_test_data_p1()[0]], 8),
    ([get_test_data_p1()[1]], 1),
    ([get_test_data_p1()[2]], 6),
    (get_test_data_p1(), 15),
    ([get_test_data_p2()[0]], 4),
    ([get_test_data_p2()[1]], 1),
    ([get_test_data_p2()[2]], 7),
    (get_test_data_p2(), 12),
])
def test_do_match(steps, expected):
    data = do_match(steps)
    assert data == expected
