import pytest

from Main import get_starting_positions, follow_trailhead_rec, calculate_trailhead_score, calculate_trailhead_rating

test_raw_data_1 = [
    '0123',
    '1234',
    '8765',
    '9876'
]

test_raw_data_2 = [
    '...0...',
    '...1...',
    '...2...',
    '6543456',
    '7.....7',
    '8.....8',
    '9.....9'
]

test_raw_data_3 = [
    '..90..9',
    '...1.98',
    '...2..7',
    '6543456',
    '765.987',
    '876....',
    '987....'
]

test_raw_data_4 = [
    '10..9..',
    '2...8..',
    '3...7..',
    '4567654',
    '...8..3',
    '...9..2',
    '.....01'
]

test_raw_data_5 = [
    '89010123',
    '78121874',
    '87430965',
    '96549874',
    '45678903',
    '32019012',
    '01329801',
    '10456732'
]

test_raw_data_6 = [
    '.....0.',
    '..4321.',
    '..5..2.',
    '..6543.',
    '..7..4.',
    '..8765.',
    '..9....'
]

test_raw_data_7 = [
    '012345',
    '123456',
    '234567',
    '345678',
    '4.6789',
    '56789.'
]


@pytest.mark.parametrize("test_map_data, expected", [
    (test_raw_data_1, [(0, 0)]),
    (test_raw_data_2, [(0, 3)]),
    (test_raw_data_3, [(0, 3)]),
    (test_raw_data_4, [(0, 1), (6, 5)]),
    (test_raw_data_5, [(0, 2), (0, 4), (2, 4), (4, 6), (5, 2), (5, 5), (6, 0), (6, 6), (7, 1)]),
])
def test_get_starting_positions(test_map_data, expected):
    data = get_starting_positions(test_map_data)
    assert data == expected


@pytest.mark.parametrize("row, col, map_data, expected", [
    (0, 0, test_raw_data_1, (16, {(3, 0)})),
    (0, 3, test_raw_data_2, (2, {(6, 6), (6, 0)})),
    (0, 3, test_raw_data_3, (13, {(4, 4), (1, 5), (0, 6), (6, 0)})),
    (0, 1, test_raw_data_4, (1, {(5, 3)})),
    (6, 5, test_raw_data_4, (2, {(5, 3), (0, 4)})),
    (0, 2, test_raw_data_5, (20, {(0, 1), (3, 4), (5, 4), (3, 0), (4, 5)})),
    (0, 4, test_raw_data_5, (24, {(0, 1), (3, 4), (5, 4), (3, 0), (4, 5), (2, 5)})),
    (2, 4, test_raw_data_5, (10, {(0, 1), (3, 4), (5, 4), (3, 0), (4, 5)})),
    (4, 6, test_raw_data_5, (4, {(4, 5), (2, 5), (3, 4)})),
    (5, 2, test_raw_data_5, (1, {(6, 4)})),
    (5, 5, test_raw_data_5, (4, {(4, 5), (2, 5), (3, 4)})),
    (6, 0, test_raw_data_5, (5, {(0, 1), (3, 4), (5, 4), (3, 0), (4, 5)})),
    (6, 6, test_raw_data_5, (8, {(4, 5), (2, 5), (3, 4)})),
    (7, 1, test_raw_data_5, (5, {(0, 1), (3, 4), (5, 4), (3, 0), (4, 5)})),
])
def test_follow_trailhead_rec(row, col, map_data, expected):
    data = follow_trailhead_rec(row, col, 0, map_data)
    assert data == expected


@pytest.mark.parametrize("map_data, expected", [
    (test_raw_data_1, 1),
    (test_raw_data_2, 2),
    (test_raw_data_3, 4),
    (test_raw_data_4, 3),
    (test_raw_data_5, 36)
])
def test_calculate_trailhead_score(map_data, expected):
    data = calculate_trailhead_score(map_data)
    assert data == expected


@pytest.mark.parametrize("map_data, expected", [
    (test_raw_data_6, 3),
    (test_raw_data_3, 13),
    (test_raw_data_7, 227),
    (test_raw_data_5, 81),
])
def test_calculate_trailhead_rating(map_data, expected):
    data = calculate_trailhead_rating(map_data)
    assert data == expected
