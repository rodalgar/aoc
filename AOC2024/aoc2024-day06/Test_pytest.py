import pytest

from Main import parse_input, traverse_map, part1, part2

test_raw_data = [
    '....#.....',
    '.........#',
    '..........',
    '..#.......',
    '.......#..',
    '..........',
    '.#..^.....',
    '........#.',
    '#.........',
    '......#...'
]


def get_test_data():
    return ((6, 4),
            0,
            [['.', '.', '.', '.', '#', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
             ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '#', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '#', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '#', '.', '.', 'O', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.', '#', '.'],
             ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '#', '.', '.', '.']])


def get_test_path():
    return ([((6, 4), None), ((5, 4), 0), ((4, 4), 0), ((3, 4), 0), ((2, 4), 0), ((1, 4), 0), ((1, 5), 1), ((1, 6), 1),
             ((1, 7), 1), ((1, 8), 1), ((2, 8), 2), ((3, 8), 2), ((4, 8), 2), ((5, 8), 2), ((6, 8), 2), ((6, 7), 3),
             ((6, 6), 3), ((6, 5), 3), ((6, 4), 3), ((6, 3), 3), ((6, 2), 3), ((5, 2), 0), ((4, 2), 0), ((4, 3), 1),
             ((4, 4), 1), ((4, 5), 1), ((4, 6), 1), ((5, 6), 2), ((6, 6), 2), ((7, 6), 2), ((8, 6), 2), ((8, 5), 3),
             ((8, 4), 3), ((8, 3), 3), ((8, 2), 3), ((8, 1), 3), ((7, 1), 0), ((7, 2), 1), ((7, 3), 1), ((7, 4), 1),
             ((7, 5), 1), ((7, 6), 1), ((7, 7), 1), ((8, 7), 2), ((9, 7), 2)],
            False)


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == get_test_data()


def test_traverse_map():
    data = traverse_map(*get_test_data(), verbose=False)
    assert data == get_test_path()


def test_part1():
    data = part1(*get_test_data())
    assert data == 41


def test_part2():
    data = part2(*get_test_data())
    assert data == 6