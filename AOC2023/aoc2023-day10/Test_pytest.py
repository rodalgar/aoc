import pytest

from Main import parse_input, map_tiles, navigate_both, get_enclosed_tiles
from Tile import Tile
from TileTemplate import TileTemplate

test_raw_data_1 = [
    '-L|F7',
    '7S-7|',
    'L|7||',
    '-L-J|',
    'L|-JF'
]

test_raw_data_2a = [
    '..F7.',
    '.FJ|.',
    'SJ.L7',
    '|F--J',
    'LJ...'
]

test_raw_data_2 = [
    '7-F7-',
    '.FJ|7',
    'SJLL7',
    '|F--J',
    'LJ.LJ'
]

test_raw_data_3 = [
    '...........',
    '.S-------7.',
    '.|F-----7|.',
    '.||.....||.',
    '.||.....||.',
    '.|L-7.F-J|.',
    '.|..|.|..|.',
    '.L--J.L--J.',
    '...........'
]

test_raw_data_4 = [
    '..........',
    '.S------7.',
    '.|F----7|.',
    '.||....||.',
    '.||....||.',
    '.|L-7F-J|.',
    '.|..||..|.',
    '.L--JL--J.',
    '..........'
]

test_raw_data_5 = [
    '.F----7F7F7F7F-7....',
    '.|F--7||||||||FJ....',
    '.||.FJ||||||||L7....',
    'FJL7L7LJLJ||LJ.L-7..',
    'L--J.L7...LJS7F-7L7.',
    '....F-J..F7FJ|L7L7L7',
    '....L7.F7||L7|.L7L7|',
    '.....|FJLJ|FJ|F7|.LJ',
    '....FJL-7.||.||||...',
    '....L---J.LJ.LJLJ...'
]

test_raw_data_6 = [
    'FF7FSF7F7F7F7F7F---7',
    'L|LJ||||||||||||F--J',
    'FL-7LJLJ||||||LJL-77',
    'F--JF--7||LJLJ7F7FJ-',
    'L---JF-JLJ.||-FJLJJ7',
    '|F|F-JF---7F7-L7L|7|',
    '|FFJF7L7F-JF7|JL---7',
    '7-L-JL7||F7|L7F-7F7|',
    'L.L7LFJ|||||FJL7||LJ',
    'L7JLJL-JLJLJL--JLJ.L'
]

test_raw_data_enclosing_1 = [
    '-L|F7',
    '7F-7|',
    '.S.||',
    '-L-J|',
    'L|-JF'
]
test_raw_data_enclosing_2 = [
    '-L|F7',
    '7F-7|',
    'L|.S|',
    '-L-J|',
    'L|-JF'
]


def get_test_data_1():
    return (1, 1), [
        [Tile(l_t('-')), Tile(l_t('L')), Tile(l_t('|')), Tile(l_t('F')), Tile(l_t('7'))],
        [Tile(l_t('7')), Tile(l_t('S')), Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('|'))],
        [Tile(l_t('L')), Tile(l_t('|')), Tile(l_t('7')), Tile(l_t('|')), Tile(l_t('|'))],
        [Tile(l_t('-')), Tile(l_t('L')), Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('|'))],
        [Tile(l_t('L')), Tile(l_t('|')), Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('F'))],
    ]


def get_test_data_2a():
    return (2, 0), [
        [Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('F')), Tile(l_t('J')), Tile(l_t('|')), Tile(l_t('.'))],
        [Tile(l_t('S')), Tile(l_t('J')), Tile(l_t('.')), Tile(l_t('L')), Tile(l_t('7'))],
        [Tile(l_t('|')), Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('J'))],
        [Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.'))]
    ]


def get_test_data_2():
    return (2, 0), [
        [Tile(l_t('7')), Tile(l_t('-')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('-'))],
        [Tile(l_t('.')), Tile(l_t('F')), Tile(l_t('J')), Tile(l_t('|')), Tile(l_t('7'))],
        [Tile(l_t('S')), Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('L')), Tile(l_t('7'))],
        [Tile(l_t('|')), Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('J'))],
        [Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('.')), Tile(l_t('L')), Tile(l_t('J'))],
    ]


def get_test_data_3():
    return (1, 1), [
        [Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')),
         Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('S')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')),
         Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')),
         Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('|')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')),
         Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')),
         Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('L')), Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('.')), Tile(l_t('F')),
         Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('|')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('.')), Tile(l_t('|')),
         Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('L')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('.')), Tile(l_t('L')),
         Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')),
         Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.'))],
    ]


def get_test_data_4():
    return (1, 1), [
        [Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')),
         Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('S')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')),
         Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')),
         Tile(l_t('7')), Tile(l_t('|')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')),
         Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')),
         Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('L')), Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('F')), Tile(l_t('-')),
         Tile(l_t('J')), Tile(l_t('|')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('.')),
         Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('L')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('-')),
         Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')),
         Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.'))],
    ]


def get_test_data_5():
    return (4, 12), [
        [Tile(l_t('.')), Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('7')),
         Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('F')),
         Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('|')),
         Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')),
         Tile(l_t('F')), Tile(l_t('J')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('.')), Tile(l_t('F')), Tile(l_t('J')), Tile(l_t('|')),
         Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')),
         Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.'))],
        [Tile(l_t('F')), Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('L')),
         Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('L')), Tile(l_t('J')),
         Tile(l_t('.')), Tile(l_t('L')), Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('.')), Tile(l_t('.'))],
        [Tile(l_t('L')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('.')), Tile(l_t('L')), Tile(l_t('7')),
         Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('S')), Tile(l_t('7')),
         Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('J')),
         Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('F')), Tile(l_t('J')), Tile(l_t('|')),
         Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('L')), Tile(l_t('7'))],
        [Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('.')),
         Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('|')),
         Tile(l_t('.')), Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('|'))],
        [Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('F')),
         Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('|')), Tile(l_t('F')), Tile(l_t('J')), Tile(l_t('|')),
         Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('|')), Tile(l_t('.')), Tile(l_t('L')), Tile(l_t('J'))],
        [Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('F')), Tile(l_t('J')), Tile(l_t('L')),
         Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('.')), Tile(l_t('|')),
         Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.'))],
        [Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('L')), Tile(l_t('-')), Tile(l_t('-')),
         Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('.')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('.')), Tile(l_t('L')),
         Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('.')), Tile(l_t('.')), Tile(l_t('.'))],
    ]


def get_test_data_6():
    return (0, 4), [
        [Tile(l_t('F')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('F')), Tile(l_t('S')), Tile(l_t('F')), Tile(l_t('7')),
         Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('F')),
         Tile(l_t('7')), Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('7'))],
        [Tile(l_t('L')), Tile(l_t('|')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')),
         Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')),
         Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('J'))],
        [Tile(l_t('F')), Tile(l_t('L')), Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('L')),
         Tile(l_t('J')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')),
         Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('7'))],
        [Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('-')),
         Tile(l_t('7')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('J')),
         Tile(l_t('7')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('F')), Tile(l_t('J')), Tile(l_t('-'))],
        [Tile(l_t('L')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('F')), Tile(l_t('-')),
         Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('.')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('-')),
         Tile(l_t('F')), Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('J')), Tile(l_t('7'))],
        [Tile(l_t('|')), Tile(l_t('F')), Tile(l_t('|')), Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('F')),
         Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('-')),
         Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('L')), Tile(l_t('|')), Tile(l_t('7')), Tile(l_t('|'))],
        [Tile(l_t('|')), Tile(l_t('F')), Tile(l_t('F')), Tile(l_t('J')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('L')),
         Tile(l_t('7')), Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('|')),
         Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('-')), Tile(l_t('7'))],
        [Tile(l_t('7')), Tile(l_t('-')), Tile(l_t('L')), Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('7')),
         Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('|')), Tile(l_t('L')), Tile(l_t('7')),
         Tile(l_t('F')), Tile(l_t('-')), Tile(l_t('7')), Tile(l_t('F')), Tile(l_t('7')), Tile(l_t('|'))],
        [Tile(l_t('L')), Tile(l_t('.')), Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('L')), Tile(l_t('F')), Tile(l_t('J')),
         Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('F')), Tile(l_t('J')),
         Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('|')), Tile(l_t('|')), Tile(l_t('L')), Tile(l_t('J'))],
        [Tile(l_t('L')), Tile(l_t('7')), Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('-')),
         Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('-')),
         Tile(l_t('-')), Tile(l_t('J')), Tile(l_t('L')), Tile(l_t('J')), Tile(l_t('.')), Tile(l_t('L'))]
    ]


def l_t(symbol: str) -> TileTemplate:
    return next((x for x in map_tiles if x.glyph == symbol), None)


@pytest.mark.parametrize("raw_data, expected_starting_position, expected_map_data", [
    (test_raw_data_1, *get_test_data_1()),
    (test_raw_data_2a, *get_test_data_2a()),
    (test_raw_data_2, *get_test_data_2()),
    (test_raw_data_3, *get_test_data_3()),
    (test_raw_data_4, *get_test_data_4()),
    (test_raw_data_5, *get_test_data_5()),
    (test_raw_data_6, *get_test_data_6())
])
def test_parse_input(raw_data, expected_starting_position, expected_map_data):
    (starting_position, map_data) = parse_input(raw_data)
    assert starting_position == expected_starting_position
    assert map_data == expected_map_data


@pytest.mark.parametrize("starting_position, map_data, expected_value", [
    (*get_test_data_1(), 4),
    (*get_test_data_2(), 8)
])
def test_navigate_both(starting_position, map_data, expected_value):
    data = navigate_both(starting_position, map_data)
    assert data == expected_value


@pytest.mark.parametrize("starting_position, map_data, expected_value", [
    (*get_test_data_3(), 4),
    (*get_test_data_4(), 4),
    (*get_test_data_5(), 8),
    (*get_test_data_6(), 10),
])
def test_get_enclosed_tiles(starting_position, map_data, expected_value):
    _ = navigate_both(starting_position, map_data, verbose=False)
    data = get_enclosed_tiles(starting_position=starting_position, navigated_map=map_data, verbose=False)
    assert data == expected_value
