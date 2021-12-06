import pytest
from Main import parse_input, process_day, process_days


def get_initial_fish_data():
    return [0, 0, 1, 1, 2, 1, 0, 0, 0, 0]


def test_parse_input():
    raw_data = '3,4,3,1,2'
    data = parse_input(raw_data)

    assert data == [0, 0, 1, 1, 2, 1, 0, 0, 0, 0]


@pytest.mark.parametrize("test_data,expected",
                         [
                             ([0, 0, 1, 1, 2, 1, 0, 0, 0, 0], [0, 1, 1, 2, 1, 0, 0, 0, 0, 0]),
                             ([0, 1, 1, 2, 1, 0, 0, 0, 0, 0], [0, 1, 2, 1, 0, 0, 0, 1, 0, 1]),
                             ([0, 1, 2, 1, 0, 0, 0, 1, 0, 1], [0, 2, 1, 0, 0, 0, 1, 1, 1, 1]),
                             ([0, 2, 1, 0, 0, 0, 1, 1, 1, 1], [0, 1, 0, 0, 0, 1, 1, 3, 1, 2])
                         ])
def test_process_day(test_data, expected):
    process_day(test_data)
    assert test_data == expected


@pytest.mark.parametrize("test_data, days, expected_fish",
                         [
                             ([0, 0, 1, 1, 2, 1, 0, 0, 0, 0], 18, 26),
                             ([0, 0, 1, 1, 2, 1, 0, 0, 0, 0], 80, 5934),
                             ([0, 0, 1, 1, 2, 1, 0, 0, 0, 0], 256, 26984457539)
                         ])
def test_process_days(test_data, days, expected_fish):
    total_fish = process_days(test_data, days)
    assert total_fish == expected_fish
