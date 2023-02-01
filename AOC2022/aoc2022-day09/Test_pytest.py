import pytest

from Main import parse_input, move_rope

test_raw_data = [
    'R 4',
    'U 4',
    'L 3',
    'D 1',
    'R 4',
    'D 1',
    'L 5',
    'R 2'
]

test_large_raw_data = [
    'R 5',
    'U 8',
    'L 8',
    'D 3',
    'R 17',
    'D 10',
    'L 25',
    'U 20'
]


def get_test_data():
    return [((0, 1), 4), ((-1, 0), 4), ((0, -1), 3), ((1, 0), 1),
            ((0, 1), 4), ((1, 0), 1), ((0, -1), 5), ((0, 1), 2)]


def get_large_test_data():
    return [((0, 1), 5), ((-1, 0), 8), ((0, -1), 8), ((1, 0), 3),
            ((0, 1), 17), ((1, 0), 10), ((0, -1), 25), ((-1, 0), 20)]


@pytest.mark.parametrize("test_data, expected", [
    (test_raw_data, get_test_data()),
    (test_large_raw_data, get_large_test_data())
])
def test_parse_input(test_data, expected):
    data = parse_input(test_data)
    assert data == expected


@pytest.mark.parametrize("test_data, n_knots, expected", [
    (get_test_data(), 2, 13),
    (get_large_test_data(), 10, 36)
])
def test_move_rope(test_data, n_knots, expected):
    data = move_rope(test_data, n_knots)
    assert len(data) == expected
