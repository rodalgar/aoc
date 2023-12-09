import pytest

from Main import parse_input, unified_extrapolate_sequence, unified_extrapolate

test_raw_data = [
    '0 3 6 9 12 15',
    '1 3 6 10 15 21',
    '10 13 16 21 30 45'
]


def get_test_data():
    return [[0, 3, 6, 9, 12, 15], [1, 3, 6, 10, 15, 21], [10, 13, 16, 21, 30, 45]]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == [[0, 3, 6, 9, 12, 15], [1, 3, 6, 10, 15, 21], [10, 13, 16, 21, 30, 45]]


@pytest.mark.parametrize("test_data, expected_first, expected_last", [
    ([0, 3, 6, 9, 12, 15], -3, 18),
    ([1, 3, 6, 10, 15, 21], 0, 28),
    ([10, 13, 16, 21, 30, 45], 5, 68)
])
def test_unified_extrapolate_sequence(test_data, expected_first, expected_last):
    data_first, data_last = unified_extrapolate_sequence(test_data)
    assert data_first == expected_first
    assert data_last == expected_last


def test_unified_extrapolate():
    data_first, data_last = unified_extrapolate(get_test_data())
    assert data_first == 2
    assert data_last == 114
