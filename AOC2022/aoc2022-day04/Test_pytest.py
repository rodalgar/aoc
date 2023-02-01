import pytest
from Main import parse_input, find_full_overlaps, find_overlaps

test_raw_data = [
    '2-4,6-8',
    '2-3,4-5',
    '5-7,7-9',
    '2-8,3-7',
    '6-6,4-6',
    '2-6,4-8'
]


def get_test_data():
    return [[range(2, 5), range(6, 9)], [range(2, 4), range(4, 6)], [range(5, 8), range(7, 10)],
            [range(2, 9), range(3, 8)], [range(6, 7), range(4, 7)], [range(2, 7), range(4, 9)]]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == get_test_data()


@pytest.mark.parametrize("test_data, expected", [
    ([[range(0, 0), range(0, 0)]], []),
    ([[range(0, 1), range(0, 1)]], [[range(0, 1), range(0, 1)]]),
    ([[range(0, 1), range(0, 1)]], [[range(0, 1), range(0, 1)]]),
    (get_test_data(), [[range(2, 9), range(3, 8)], [range(6, 7), range(4, 7)]])
])
def test_find_full_overlaps(test_data, expected):
    data = find_full_overlaps(test_data)
    assert data == expected


@pytest.mark.parametrize("test_data, expected", [
    ([[range(0, 0), range(0, 0)]], []),
    ([[range(0, 1), range(0, 1)]], [[range(0, 1), range(0, 1)]]),
    (get_test_data(), [[range(5, 8), range(7, 10)],
                       [range(2, 9), range(3, 8)],
                       [range(6, 7), range(4, 7)],
                       [range(2, 7), range(4, 9)]])
])
def test_find_overlaps(test_data, expected):
    data = find_overlaps(test_data)
    assert data == expected
