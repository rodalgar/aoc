import pytest

from Main import parse_input, search_minimums, calculate_risks, get_basin_from, get_largest_basins

raw_test_data = [
    '2199943210',
    '3987894921',
    '9856789892',
    '8767896789',
    '9899965678'
]


def get_test_data():
    return [[2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
            [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
            [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
            [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
            [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]]


def get_test_minimums():
    return [(0, 1, 1), (0, 9, 0), (2, 2, 5), (4, 6, 5)]


def test_parse_input():
    data = parse_input(raw_test_data)
    assert data == [[2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
                    [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
                    [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
                    [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
                    [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]]


def test_search_minimums():
    data = search_minimums(get_test_data())
    assert data == [(0, 1, 1), (0, 9, 0), (2, 2, 5), (4, 6, 5)]


def test_calculate_risks():
    data = calculate_risks(get_test_minimums())
    assert data == 15


@pytest.mark.parametrize("starting_row, starting_col, expected",
                         [
                             (0, 1, [(0, 1), (0, 0), (1, 0)]),
                             (0, 9, [(0, 9), (0, 8), (1, 9), (0, 7), (1, 8), (2, 9), (0, 6), (0, 5), (1, 6)]),
                             (2, 2,
                              [(2, 2), (1, 2), (2, 1), (3, 2), (2, 3), (1, 3), (3, 1), (3, 3), (2, 4), (1, 4), (3, 0),
                               (4, 1), (3, 4), (2, 5)]),
                             (4, 6, [(4, 6), (3, 6), (4, 5), (4, 7), (3, 7), (4, 8), (2, 7), (3, 8), (4, 9)])
                         ])
def test_get_basin_from(starting_row, starting_col, expected):
    data = get_basin_from(get_test_data(), starting_row, starting_col)
    assert data == expected


def test_get_largest_basins():
    data = get_largest_basins(get_test_data(), get_test_minimums())
    assert data == 1134
