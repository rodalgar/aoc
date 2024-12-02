import pytest

from Main import parse_input, analyze_report, analyze_all

test_raw_data = [
    '7 6 4 2 1',
    '1 2 7 8 9',
    '9 7 6 2 1',
    '1 3 2 4 5',
    '8 6 4 4 1',
    '1 3 6 7 9'
]


def get_test_data():
    return [[7, 6, 4, 2, 1], [1, 2, 7, 8, 9], [9, 7, 6, 2, 1], [1, 3, 2, 4, 5], [8, 6, 4, 4, 1], [1, 3, 6, 7, 9]]


def get_own_test_data():
    return [2, 1, 2, 3]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == get_test_data()


@pytest.mark.parametrize("test_data, expected", [
    (get_test_data()[0], True),
    (get_test_data()[1], False),
    (get_test_data()[2], False),
    (get_test_data()[3], False),
    (get_test_data()[4], False),
    (get_test_data()[5], True),
    (get_own_test_data(), False)
])
def test_analyze_report(test_data, expected):
    data = analyze_report(test_data)
    assert data[0] == expected


@pytest.mark.parametrize("test_data, use_problem_dampener, expected", [
    (get_test_data(), False, 2),
    (get_test_data(), True, 4),
    ([get_own_test_data()], False, 0),
    ([get_own_test_data()], True, 1),
])
def test_analyze_all(test_data, use_problem_dampener, expected):
    data = analyze_all(test_data, use_problem_dampener)
    assert data == expected
