import pytest

from Main import parse_input, get_distance, get_similarity_score

test_raw_data = [
    '3   4',
    '4   3',
    '2   5',
    '1   3',
    '3   9',
    '3   3'
]


def get_test_data():
    return [3, 4, 2, 1, 3, 3], [4, 3, 5, 3, 9, 3]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == get_test_data()


def test_get_distance():
    data = get_distance(*get_test_data())
    assert data == 11


def test_get_similarity_score():
    data = get_similarity_score(*get_test_data())
    assert data == 31
