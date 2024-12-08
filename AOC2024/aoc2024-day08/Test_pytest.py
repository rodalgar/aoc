import pytest

from Main import parse_input, Antenna, calculate_distances, calculate_antinodes, Antinode, \
    calculate_antinodes_with_resonance, calculate_impact, part1, part2

test_raw_data_1 = [
    '..........',
    '..........',
    '..........',
    '....a.....',
    '..........',
    '.....a....',
    '..........',
    '..........',
    '..........',
    '..........'
]

test_raw_data_2 = [
    '..........',
    '..........',
    '..........',
    '....a.....',
    '........a.',
    '.....a....',
    '..........',
    '..........',
    '..........',
    '..........'
]

test_raw_data_big_1 = [
    '............',
    '........0...',
    '.....0......',
    '.......0....',
    '....0.......',
    '......A.....',
    '............',
    '............',
    '........A...',
    '.........A..',
    '............',
    '............'
]

test_raw_data_3 = [
    'T.........',
    '...T......',
    '.T........',
    '..........',
    '..........',
    '..........',
    '..........',
    '..........',
    '..........',
    '..........'
]


def get_test_data_1():
    return {'a': [Antenna(id=0, row=3, col=4), Antenna(id=1, row=5, col=5)]}, (10, 10)


def get_test_data_2():
    return {'a': [Antenna(id=0, row=3, col=4),
                  Antenna(id=1, row=4, col=8),
                  Antenna(id=2, row=5, col=5)]}, (10, 10)


def get_test_data_3():
    return {'T': [Antenna(id=0, row=0, col=0),
                  Antenna(id=1, row=1, col=3),
                  Antenna(id=2, row=2, col=1)]}, (10, 10)


def get_test_data_big():
    return {'0': [Antenna(id=0, row=1, col=8),
                  Antenna(id=1, row=2, col=5),
                  Antenna(id=2, row=3, col=7),
                  Antenna(id=3, row=4, col=4)],
            'A': [Antenna(id=0, row=5, col=6),
                  Antenna(id=1, row=8, col=8),
                  Antenna(id=2, row=9, col=9)]}, (12, 12)


def get_distances_1():
    return {'a': [(0, 1, -2, -1)]}


def get_distances_2():
    return {'a': [(0, 1, -1, -4), (0, 2, -2, -1), (1, 2, -1, 3)]}


def get_distances_3():
    return {'T': [(0, 1, -1, -3), (0, 2, -2, -1), (1, 2, -1, 2)]}


def get_distances_big():
    return {'0': [(0, 1, -1, 3), (0, 2, -2, 1), (0, 3, -3, 4),
                  (1, 2, -1, -2), (1, 3, -2, 1), (2, 3, -1, 3)],
            'A': [(0, 1, -3, -2), (0, 2, -4, -3), (1, 2, -1, -1)]}


def get_antinodes_1():
    return {'a': [Antinode(id=0, l_antenna=0, r_antenna=1, row=1, col=3),
                  Antinode(id=1, l_antenna=0, r_antenna=1, row=7, col=6)]}


def get_antinodes_2():
    return {'a': [Antinode(id=0, l_antenna=0, r_antenna=1, row=2, col=0),
                  Antinode(id=1, l_antenna=0, r_antenna=2, row=1, col=3),
                  Antinode(id=2, l_antenna=0, r_antenna=2, row=7, col=6),
                  Antinode(id=3, l_antenna=1, r_antenna=2, row=6, col=2)]}


def get_antinodes_big():
    return {'0': [Antinode(id=0, l_antenna=0, r_antenna=1, row=0, col=11),
                  Antinode(id=1, l_antenna=0, r_antenna=1, row=3, col=2),
                  Antinode(id=2, l_antenna=0, r_antenna=2, row=5, col=6),
                  Antinode(id=3, l_antenna=0, r_antenna=3, row=7, col=0),
                  Antinode(id=4, l_antenna=1, r_antenna=2, row=1, col=3),
                  Antinode(id=5, l_antenna=1, r_antenna=2, row=4, col=9),
                  Antinode(id=6, l_antenna=1, r_antenna=3, row=0, col=6),
                  Antinode(id=7, l_antenna=1, r_antenna=3, row=6, col=3),
                  Antinode(id=8, l_antenna=2, r_antenna=3, row=2, col=10),
                  Antinode(id=9, l_antenna=2, r_antenna=3, row=5, col=1)],
            'A': [Antinode(id=0, l_antenna=0, r_antenna=1, row=2, col=4),
                  Antinode(id=1, l_antenna=0, r_antenna=1, row=11, col=10),
                  Antinode(id=2, l_antenna=0, r_antenna=2, row=1, col=3),
                  Antinode(id=3, l_antenna=1, r_antenna=2, row=7, col=7),
                  Antinode(id=4, l_antenna=1, r_antenna=2, row=10, col=10)]}


def get_antinodes_with_resonance_3():
    return {'T': [Antinode(id=0, l_antenna=0, r_antenna=1, row=2, col=6),
                  Antinode(id=1, l_antenna=0, r_antenna=1, row=3, col=9),
                  Antinode(id=2, l_antenna=0, r_antenna=2, row=4, col=2),
                  Antinode(id=3, l_antenna=0, r_antenna=2, row=6, col=3),
                  Antinode(id=4, l_antenna=0, r_antenna=2, row=8, col=4),
                  Antinode(id=5, l_antenna=1, r_antenna=2, row=0, col=5),
                  Antinode(id=6, l_antenna=1, r_antenna=1, row=1, col=3),
                  Antinode(id=7, l_antenna=0, r_antenna=0, row=0, col=0),
                  Antinode(id=8, l_antenna=2, r_antenna=2, row=2, col=1)]}


def get_antinodes_with_resonance_big():
    return {'0': [Antinode(id=0, l_antenna=0, r_antenna=1, row=0, col=11),
                  Antinode(id=1, l_antenna=0, r_antenna=1, row=3, col=2),
                  Antinode(id=2, l_antenna=0, r_antenna=2, row=5, col=6),
                  Antinode(id=3, l_antenna=0, r_antenna=2, row=7, col=5),
                  Antinode(id=4, l_antenna=0, r_antenna=2, row=9, col=4),
                  Antinode(id=5, l_antenna=0, r_antenna=2, row=11, col=3),
                  Antinode(id=6, l_antenna=0, r_antenna=3, row=7, col=0),
                  Antinode(id=7, l_antenna=1, r_antenna=2, row=1, col=3),
                  Antinode(id=8, l_antenna=1, r_antenna=2, row=0, col=1),
                  Antinode(id=9, l_antenna=1, r_antenna=2, row=4, col=9),
                  Antinode(id=10, l_antenna=1, r_antenna=2, row=5, col=11),
                  Antinode(id=11, l_antenna=1, r_antenna=3, row=0, col=6),
                  Antinode(id=12, l_antenna=1, r_antenna=3, row=6, col=3),
                  Antinode(id=13, l_antenna=1, r_antenna=3, row=8, col=2),
                  Antinode(id=14, l_antenna=1, r_antenna=3, row=10, col=1),
                  Antinode(id=15, l_antenna=2, r_antenna=3, row=2, col=10),
                  Antinode(id=16, l_antenna=2, r_antenna=3, row=5, col=1),
                  Antinode(id=17, l_antenna=0, r_antenna=0, row=1, col=8),
                  Antinode(id=18, l_antenna=2, r_antenna=2, row=3, col=7),
                  Antinode(id=19, l_antenna=3, r_antenna=3, row=4, col=4),
                  Antinode(id=20, l_antenna=1, r_antenna=1, row=2, col=5)],
            'A': [Antinode(id=0, l_antenna=0, r_antenna=1, row=2, col=4),
                  Antinode(id=1, l_antenna=0, r_antenna=1, row=11, col=10),
                  Antinode(id=2, l_antenna=0, r_antenna=2, row=1, col=3),
                  Antinode(id=3, l_antenna=1, r_antenna=2, row=7, col=7),
                  Antinode(id=4, l_antenna=1, r_antenna=2, row=6, col=6),
                  Antinode(id=5, l_antenna=1, r_antenna=2, row=5, col=5),
                  Antinode(id=6, l_antenna=1, r_antenna=2, row=4, col=4),
                  Antinode(id=7, l_antenna=1, r_antenna=2, row=3, col=3),
                  Antinode(id=8, l_antenna=1, r_antenna=2, row=2, col=2),
                  Antinode(id=9, l_antenna=1, r_antenna=2, row=1, col=1),
                  Antinode(id=10, l_antenna=1, r_antenna=2, row=0, col=0),
                  Antinode(id=11, l_antenna=1, r_antenna=2, row=10, col=10),
                  Antinode(id=12, l_antenna=1, r_antenna=2, row=11, col=11),
                  Antinode(id=13, l_antenna=0, r_antenna=0, row=5, col=6),
                  Antinode(id=14, l_antenna=1, r_antenna=1, row=8, col=8),
                  Antinode(id=15, l_antenna=2, r_antenna=2, row=9, col=9)]}


def get_impact_2():
    return {(1, 3), (6, 2), (7, 6), (2, 0)}


def get_impact_big():
    return {(0, 6), (0, 11), (1, 3), (2, 4), (2, 10), (3, 2), (4, 9), (5, 1),
            (5, 6), (6, 3), (7, 0), (7, 7), (10, 10), (11, 10)}


def get_impact_3():
    return {(8, 4), (2, 1), (0, 0), (4, 2), (2, 6), (3, 9), (0, 5), (6, 3), (1, 3)}


def get_impact_big_with_resonance():
    return {(0, 0), (0, 1), (0, 6), (0, 11), (1, 1), (1, 3), (1, 8), (2, 2), (2, 4), (2, 5), (2, 10), (3, 2), (3, 3),
            (3, 7), (4, 4), (4, 9), (5, 1), (5, 5), (5, 6), (5, 11), (6, 3), (6, 6), (7, 0), (7, 5), (7, 7), (8, 2),
            (8, 8), (9, 4), (9, 9), (10, 1), (10, 10), (11, 3), (11, 10), (11, 11)}


@pytest.mark.parametrize("raw_data,expected", [
    (test_raw_data_1, get_test_data_1()),
    (test_raw_data_2, get_test_data_2()),
    (test_raw_data_3, get_test_data_3()),
    (test_raw_data_big_1, get_test_data_big()),
])
def test_parse_input(raw_data, expected):
    data = parse_input(raw_data)
    assert data == expected


@pytest.mark.parametrize("antennas,expected", [
    (get_test_data_1()[0], get_distances_1()),
    (get_test_data_2()[0], get_distances_2()),
    (get_test_data_3()[0], get_distances_3()),
    (get_test_data_big()[0], get_distances_big()),
])
def test_calculate_distances(antennas, expected):
    data = calculate_distances(antennas)
    assert data == expected


@pytest.mark.parametrize("antennas,distances,map_geometry,expected", [
    (get_test_data_1()[0], get_distances_1(), get_test_data_1()[1], get_antinodes_1()),
    (get_test_data_2()[0], get_distances_2(), get_test_data_2()[1], get_antinodes_2()),
    (get_test_data_big()[0], get_distances_big(), get_test_data_big()[1], get_antinodes_big())
])
def test_calculate_antinodes(antennas, distances, map_geometry, expected):
    data = calculate_antinodes(antennas, distances, map_geometry)
    assert data == expected


@pytest.mark.parametrize("antennas, distances, map_geometry, expected", [
    (get_test_data_3()[0], get_distances_3(), get_test_data_3()[1], get_antinodes_with_resonance_3()),
    (get_test_data_big()[0], get_distances_big(), get_test_data_big()[1], get_antinodes_with_resonance_big())
])
def test_calculate_antinodes_with_resonance(antennas, distances, map_geometry, expected):
    data = calculate_antinodes_with_resonance(antennas, distances, map_geometry)
    assert data == expected


@pytest.mark.parametrize("antinodes,expected", [
    (get_antinodes_2(), get_impact_2()),
    (get_antinodes_big(), get_impact_big()),
    (get_antinodes_with_resonance_3(), get_impact_3()),
    (get_antinodes_with_resonance_big(), get_impact_big_with_resonance())
])
def test_calculate_impact(antinodes, expected):
    data = calculate_impact(antinodes)
    assert data == expected


def test_part1():
    data = part1(*get_test_data_big())
    assert data == 14


def test_part2():
    data = part2(*get_test_data_big())
    assert data == 34
