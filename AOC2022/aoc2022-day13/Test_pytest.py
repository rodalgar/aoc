import pytest

from Main import parse_input, compare, part1, part2, RIGHT_ORDER, NOT_RIGHT_ORDER, UNDETERMINED_ORDER

test_raw_data = [
    '[1,1,3,1,1]',
    '[1,1,5,1,1]',
    '',
    '[[1],[2,3,4]]',
    '[[1],4]',
    '',
    '[9]',
    '[[8,7,6]]',
    '',
    '[[4,4],4,4]',
    '[[4,4],4,4,4]',
    '',
    '[7,7,7,7]',
    '[7,7,7]',
    '',
    '[]',
    '[3]',
    '',
    '[[[]]]',
    '[[]]',
    '',
    '[1,[2,[3,[4,[5,6,7]]]],8,9]',
    '[1,[2,[3,[4,[5,6,0]]]],8,9]'
]


def get_test_data():
    return [[1, 1, 3, 1, 1],
            [1, 1, 5, 1, 1],
            [[1], [2, 3, 4]],
            [[1], 4],
            [9],
            [[8, 7, 6]],
            [[4, 4], 4, 4],
            [[4, 4], 4, 4, 4],
            [7, 7, 7, 7],
            [7, 7, 7],
            [],
            [3],
            [[[]]],
            [[]],
            [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
            [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == get_test_data()


@pytest.mark.parametrize("left, right, expected", [
    (get_test_data()[0], get_test_data()[1], RIGHT_ORDER),
    (get_test_data()[2], get_test_data()[3], RIGHT_ORDER),
    (get_test_data()[4], get_test_data()[5], NOT_RIGHT_ORDER),
    (get_test_data()[6], get_test_data()[7], RIGHT_ORDER),
    (get_test_data()[8], get_test_data()[9], NOT_RIGHT_ORDER),
    (get_test_data()[10], get_test_data()[11], RIGHT_ORDER),
    (get_test_data()[12], get_test_data()[13], NOT_RIGHT_ORDER),
    (get_test_data()[14], get_test_data()[15], NOT_RIGHT_ORDER),
    (get_test_data()[0], get_test_data()[0], UNDETERMINED_ORDER),
    (get_test_data()[1], get_test_data()[0], NOT_RIGHT_ORDER)
])
def test_compare(left, right, expected):
    data = compare(left, right)
    assert data == expected


def test_part1():
    data = part1(get_test_data())
    assert data == 13


def test_part2():
    _, _, data = part2(get_test_data())
    assert data == 140
