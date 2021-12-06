import pytest
from Main import parse_input, is_horizontal, is_vertical, is_ascending_slope, is_descending_slope, sort_lines, \
    expand_lines, search_intersections


def test_parse_input():
    test_data = [
        '0,9 -> 5,9',  #
        '8,0 -> 0,8',
        '9,4 -> 3,4',  #
        '2,2 -> 2,1',  #
        '7,0 -> 7,4',  #
        '6,4 -> 2,0',
        '0,9 -> 2,9',  #
        '3,4 -> 1,4',  #
        '0,0 -> 8,8',
        '5,5 -> 8,2'
    ]
    data = parse_input(test_data)
    assert data == [(0, 9, 5, 9), (8, 0, 0, 8), (9, 4, 3, 4), (2, 2, 2, 1), (7, 0, 7, 4), (6, 4, 2, 0), (0, 9, 2, 9),
                    (3, 4, 1, 4), (0, 0, 8, 8), (5, 5, 8, 2)]


@pytest.mark.parametrize("line,expected",
                         [
                             ((0, 9, 5, 9), True),
                             ((9, 4, 3, 4), True),
                             ((2, 2, 2, 1), False),
                             ((7, 0, 7, 4), False),
                             ((6, 4, 2, 0), False),
                             ((0, 9, 2, 9), True),
                             ((3, 4, 1, 4), True),
                             ((0, 0, 8, 8), False),
                             ((5, 5, 8, 2), False),
                             ((8, 0, 0, 8), False)
                         ])
def test_is_horizontal(line, expected):
    data = is_horizontal(line)
    assert data == expected


@pytest.mark.parametrize("line,expected",
                         [
                             ((8, 0, 0, 8), False),
                             ((2, 2, 2, 1), True),
                             ((7, 0, 7, 4), True),
                             ((6, 4, 2, 0), False),
                             ((0, 0, 8, 8), False),
                             ((5, 5, 8, 2), False)
                         ])
def test_is_vertical(line, expected):
    data = is_vertical(line)
    assert data == expected


@pytest.mark.parametrize("line,expected",
                         [
                             ((8, 0, 0, 8), False),
                             ((6, 4, 2, 0), True),
                             ((0, 0, 8, 8), True),
                             ((5, 5, 8, 2), False),
                             ((0, 8, 8, 0), False),
                             ((2, 0, 6, 4), True),
                             ((0, 0, 8, 8), True),
                             ((5, 5, 8, 2), False)
                         ])
def test_is_ascending_slope(line, expected):
    data = is_ascending_slope(line)
    assert data == expected


@pytest.mark.parametrize("line,expected",
                         [
                             ((8, 0, 0, 8), True),
                             ((5, 5, 8, 2), True),
                             ((0, 8, 8, 0), True),
                             ((5, 5, 8, 2), True)
                         ])
def test_is_descending_slope(line, expected):
    data = is_descending_slope(line)
    assert data == expected


@pytest.mark.parametrize("lines,add_slope,expected",
                         [
                             ([(0, 9, 5, 9), (8, 0, 0, 8), (9, 4, 3, 4), (2, 2, 2, 1), (7, 0, 7, 4), (6, 4, 2, 0),
                               (0, 9, 2, 9), (3, 4, 1, 4), (0, 0, 8, 8), (5, 5, 8, 2)], False,
                              [(0, 9, 5, 9), (8, 0, 0, 8), (3, 4, 9, 4), (2, 1, 2, 2), (7, 0, 7, 4), (6, 4, 2, 0),
                               (0, 9, 2, 9), (1, 4, 3, 4),
                               (0, 0, 8, 8), (5, 5, 8, 2)]
                              ),
                             ([(0, 9, 5, 9), (8, 0, 0, 8), (9, 4, 3, 4), (2, 2, 2, 1), (7, 0, 7, 4), (6, 4, 2, 0),
                               (0, 9, 2, 9), (3, 4, 1, 4), (0, 0, 8, 8), (5, 5, 8, 2)], True,
                              [(0, 9, 5, 9), (0, 8, 8, 0), (3, 4, 9, 4), (2, 1, 2, 2), (7, 0, 7, 4), (2, 0, 6, 4),
                               (0, 9, 2, 9), (1, 4, 3, 4), (0, 0, 8, 8), (5, 5, 8, 2)])
                         ])
def test_sort_lines(lines, add_slope, expected):
    data = sort_lines(lines, add_slope)
    assert data == expected


@pytest.mark.parametrize("lines,add_slope,expected",
                         [
                             ([(0, 9, 5, 9), (8, 0, 0, 8), (9, 4, 3, 4), (2, 2, 2, 1), (7, 0, 7, 4), (6, 4, 2, 0),
                               (0, 9, 2, 9), (3, 4, 1, 4), (0, 0, 8, 8), (5, 5, 8, 2)], False,
                              [[(0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9)],
                               [(3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4)], [(2, 1), (2, 2)],
                               [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4)], [(0, 9), (1, 9), (2, 9)],
                               [(1, 4), (2, 4), (3, 4)]]),
                             ([(0, 9, 5, 9), (8, 0, 0, 8), (9, 4, 3, 4), (2, 2, 2, 1), (7, 0, 7, 4), (6, 4, 2, 0),
                               (0, 9, 2, 9), (3, 4, 1, 4), (0, 0, 8, 8), (5, 5, 8, 2)], True,
                              [[(0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9)],
                               [(0, 8), (1, 7), (2, 6), (3, 5), (4, 4), (5, 3), (6, 2), (7, 1), (8, 0)],
                               [(3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4)], [(2, 1), (2, 2)],
                               [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4)], [(2, 0), (3, 1), (4, 2), (5, 3), (6, 4)],
                               [(0, 9), (1, 9), (2, 9)], [(1, 4), (2, 4), (3, 4)],
                               [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)],
                               [(5, 5), (6, 4), (7, 3), (8, 2)]]
                              )
                         ])
def test_expand_lines(lines, add_slope, expected):
    data = expand_lines(lines, add_slope)
    assert data == expected


def test_search_intersections():
    test_expanded_lines = [[(0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9)],
                           [(0, 8), (1, 7), (2, 6), (3, 5), (4, 4), (5, 3), (6, 2), (7, 1), (8, 0)],
                           [(3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4)], [(2, 1), (2, 2)],
                           [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4)], [(2, 0), (3, 1), (4, 2), (5, 3), (6, 4)],
                           [(0, 9), (1, 9), (2, 9)], [(1, 4), (2, 4), (3, 4)],
                           [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)],
                           [(5, 5), (6, 4), (7, 3), (8, 2)]]
    expected_intersections = {'0-9': 1, '1-9': 1, '2-9': 1, '4-4': 3, '7-1': 1, '5-3': 1, '7-4': 1, '6-4': 3, '3-4': 1,
                              '2-2': 1, '7-3': 1, '5-5': 1}
    data = search_intersections(test_expanded_lines)
    assert data == expected_intersections
