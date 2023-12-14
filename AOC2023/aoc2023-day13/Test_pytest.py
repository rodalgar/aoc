import pytest

from Main import parse_input, locate_mirror_in_pattern, locate_mirrors, locate_smudge_in_pattern, part1, part2

test_raw_data = [
    '#.##..##.',
    '..#.##.#.',
    '##......#',
    '##......#',
    '..#.##.#.',
    '..##..##.',
    '#.#.##.#.',
    '',
    '#...##..#',
    '#....#..#',
    '..##..###',
    '#####.##.',
    '#####.##.',
    '..##..###',
    '#....#..#'
]


def get_test_data_1():
    return (['#.##..##.',
             '..#.##.#.',
             '##......#',
             '##......#',
             '..#.##.#.',
             '..##..##.',
             '#.#.##.#.'],
            ['#.##..#',
             '..##...',
             '##..###',
             '#....#.',
             '.#..#.#',
             '.#..#.#',
             '#....#.',
             '##..###',
             '..##...'])


def get_test_data_2():
    return (['#...##..#',
             '#....#..#',
             '..##..###',
             '#####.##.',
             '#####.##.',
             '..##..###',
             '#....#..#'],
            ['##.##.#',
             '...##..',
             '..####.',
             '..####.',
             '#..##..',
             '##....#',
             '..####.',
             '..####.',
             '###..##'])


def get_test_data():
    return [get_test_data_1(), get_test_data_2()]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == get_test_data()


@pytest.mark.parametrize("test_data, expected", [
    (get_test_data_1()[0], None),
    (get_test_data_1()[1], (5, 6)),
    (get_test_data_2()[0], (4, 5)),
    (get_test_data_2()[1], None),
])
def test_locate_mirror_in_pattern(test_data, expected):
    data = locate_mirror_in_pattern(test_data)
    assert data == expected


@pytest.mark.parametrize("test_data, mirror_data, expected", [
    (get_test_data_1()[0], None, (3, 4)),
    (get_test_data_1()[1], 5, None),
    (get_test_data_2()[0], 4, (1, 2)),
    (get_test_data_2()[1], None, None),
])
def test_locate_smudge_in_pattern(test_data, mirror_data, expected):
    data = locate_smudge_in_pattern(test_data, mirror_line=mirror_data)
    assert data == expected


@pytest.mark.parametrize("test_data, expected", [
    (get_test_data_1(), (0, (5, 6),
                         ['#.##..##.',
                          '..#.##.#.',
                          '##......#',
                          '##......#',
                          '..#.##.#.',
                          '..##..##.',
                          '#.#.##.#.'],
                         ['#.##..#',
                          '..##...',
                          '##..###',
                          '#....#.',
                          '.#..#.#',
                          '.#..#.#',
                          '#....#.',
                          '##..###',
                          '..##...'])),
    (get_test_data_2(), (1, (4, 5),
                         ['#...##..#',
                          '#....#..#',
                          '..##..###',
                          '#####.##.',
                          '#####.##.',
                          '..##..###',
                          '#....#..#'],
                         ['##.##.#',
                          '...##..',
                          '..####.',
                          '..####.',
                          '#..##..',
                          '##....#',
                          '..####.',
                          '..####.',
                          '###..##']))
])
def test_locate_mirrors(test_data, expected):
    data = locate_mirrors(test_data)
    assert data == expected


def test_part1():
    data = part1(get_test_data())
    assert data == 405


def test_part2():
    data = part2(get_test_data())
    assert data == 400
