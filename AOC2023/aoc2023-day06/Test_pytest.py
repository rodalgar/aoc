import pytest

from Main import parse_input_part1, parse_input_part2, calculate, accrue_times

test_raw_data = [
    'Time:      7  15   30',
    'Distance:  9  40  200'
]


def test_parse_input_part1():
    data = parse_input_part1(test_raw_data)
    assert data == [(7, 9), (15, 40), (30, 200)]


def test_parse_input_part2():
    data = parse_input_part2(test_raw_data)
    assert data == [(71530, 940200)]


@pytest.mark.parametrize("time, record, expected", [
    (7, 9, 4),
    (15, 40, 8),
    (30, 200, 9),
    (71530, 940200, 71503)
])
def test_calculate(time, record, expected):
    data = calculate(time, record)
    assert data == expected


@pytest.mark.parametrize("values, expected", [
    ([(7, 9), (15, 40), (30, 200)], 288),
    ([(71530, 940200)], 71503)
])
def test_accrue_times(values, expected):
    data = accrue_times(values)
    assert data == expected
