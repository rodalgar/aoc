import pytest

from Main import get_numbers_from_line, part1, get_numbers_from_line_v2, extract_number, part2, numbers

test_raw_data = [
    '1abc2',
    'pqr3stu8vwx',
    'a1b2c3d4e5f',
    'treb7uchet'
]

test_raw_data_2 = [
    'two1nine',
    'eightwothree',
    'abcone2threexyz',
    'xtwone3four',
    '4nineeightseven2',
    'zoneight234',
    '7pqrstsixteen'
]


@pytest.mark.parametrize("raw_data, expected", [
    (test_raw_data[0], 12),
    (test_raw_data[1], 38),
    (test_raw_data[2], 15),
    (test_raw_data[3], 77)
])
def test_get_numbers_from_line(raw_data, expected):
    data = get_numbers_from_line(raw_data)
    assert data == expected


def test_part1():
    data = part1(test_raw_data)
    assert data == 142


@pytest.mark.parametrize("raw_data, expected", [
    (test_raw_data_2[0], 29),
    (test_raw_data_2[1], 83),
    (test_raw_data_2[2], 13),
    (test_raw_data_2[3], 24),
    (test_raw_data_2[4], 42),
    (test_raw_data_2[5], 14),
    (test_raw_data_2[6], 76)
])
def test_get_numbers_from_line_v2(raw_data, expected):
    data = get_numbers_from_line_v2(raw_data)
    assert data == expected


@pytest.mark.parametrize("raw_data, index, expected", [
    ('two1nine', 0, 2),
    ('two1nine', 1, None),
    ('two1nine', 2, None),
    ('two1nine', 3, None),
    ('two1nine', 4, 9),
    ('two1nine', 5, None),
    ('two1nine', 6, None),
    ('two1nine', 7, None),
])
def test_extract_number(raw_data, index, expected):
    data = extract_number(raw_data, index, numbers)
    assert data == expected


def test_part2():
    data = part2(test_raw_data_2)
    assert data == 281
