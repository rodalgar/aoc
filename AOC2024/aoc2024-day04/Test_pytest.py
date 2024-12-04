import pytest

from Main import find_xmas, find_x_mas

test_raw_data = [
    'MMMSXXMASM',
    'MSAMXMSMSA',
    'AMXSXMAAMM',
    'MSAMASMSMX',
    'XMASAMXAMM',
    'XXAMMXXAMA',
    'SMSMSASXSS',
    'SAXAMASAAA',
    'MAMMMXMMMM',
    'MXMXAXMASX'
]


def test_find_xmas():
    data = find_xmas(test_raw_data)
    assert data == 18


def test_find_x_mas():
    data = find_x_mas(test_raw_data)
    assert data == 9
