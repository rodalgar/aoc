import pytest

from Main import parse_input, range_part1, range_part2, range_map_stage, range_map_stages

test_raw_data = [
    'seeds: 79 14 55 13',
    '',
    'seed-to-soil map:',
    '50 98 2',
    '52 50 48',
    '',
    'soil-to-fertilizer map:',
    '0 15 37',
    '37 52 2',
    '39 0 15',
    '',
    'fertilizer-to-water map:',
    '49 53 8',
    '0 11 42',
    '42 0 7',
    '57 7 4',
    '',
    'water-to-light map:',
    '88 18 7',
    '18 25 70',
    '',
    'light-to-temperature map:',
    '45 77 23',
    '81 45 19',
    '68 64 13',
    '',
    'temperature-to-humidity map:',
    '0 69 1',
    '1 0 69',
    '',
    'humidity-to-location map:',
    '60 56 37',
    '56 93 4'
]


def get_test_seeds():
    return [79, 14, 55, 13]


def get_test_seeds_part1():
    return [(79, 1), (14, 1), (55, 1), (13, 1)]


def get_test_seeds_part2():
    return [(79, 14), (55, 13)]


def get_test_mapping():
    return ['seed',
            'soil',
            [(52, 50, 48), (50, 98, 2)],
            ['soil',
             'fertilizer',
             [(39, 0, 15), (0, 15, 37), (37, 52, 2)],
             ['fertilizer',
              'water',
              [(42, 0, 7), (57, 7, 4), (0, 11, 42), (49, 53, 8)],
              ['water',
               'light',
               [(88, 18, 7), (18, 25, 70)],
               ['light',
                'temperature',
                [(81, 45, 19), (68, 64, 13), (45, 77, 23)],
                ['temperature',
                 'humidity',
                 [(1, 0, 69), (0, 69, 1)],
                 ['humidity', 'location', [(60, 56, 37), (56, 93, 4)], None]]]]]]]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == (get_test_seeds(), get_test_mapping())


def test_range_map_stage_part1():
    data = range_map_stage(get_test_seeds_part1(), get_test_mapping())
    assert data == [(81, 1), (14, 1), (55, 1), (13, 1)]


def test_range_map_stage_part2():
    data = range_map_stage(get_test_seeds_part2(), get_test_mapping())
    assert data == [(81, 14), (55, 13)]


def test_range_map_stages_part1():
    data = range_map_stages(get_test_seeds_part1(), get_test_mapping())
    assert data == [(35, 1), (43, 1), (82, 1), (86, 1)]


def test_range_map_stages_part2():
    data = range_map_stages(get_test_seeds_part2(), get_test_mapping())
    assert data == [(46, 10), (60, 1), (82, 3), (86, 4), (94, 3), (56, 4), (97, 2)]


def test_range_part1():
    data = range_part1(get_test_seeds(), get_test_mapping())
    assert data == 35


def test_range_part2():
    data = range_part2(get_test_seeds(), get_test_mapping())
    assert data == 46
