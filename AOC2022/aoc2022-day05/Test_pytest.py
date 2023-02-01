import pytest
from Main import parse_input, get_tops, move_things

test_raw_data = [
    '    [D]    ',
    '[N] [C]    ',
    '[Z] [M] [P]',
    ' 1   2   3 ',
    '',
    'move 1 from 2 to 1',
    'move 3 from 1 to 3',
    'move 2 from 2 to 1',
    'move 1 from 1 to 2',
]


def get_test_data():
    return ([['N', 'Z'], ['D', 'C', 'M'], ['P']],
            [(1, 1, 0), (3, 0, 2), (2, 1, 0), (1, 0, 1)])


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == ([['N', 'Z'], ['D', 'C', 'M'], ['P']],
                    [(1, 1, 0), (3, 0, 2), (2, 1, 0), (1, 0, 1)])


def test_move_things_p1():
    yard, instructions = get_test_data()
    data = move_things(yard, instructions)
    assert data == [['C'], ['M'], ['Z', 'N', 'D', 'P']]


def test_move_things_p2():
    yard, instructions = get_test_data()
    data = move_things(yard, instructions, reverse_items=False)
    assert data == [['M'], ['C'], ['D', 'N', 'Z', 'P']]


@pytest.mark.parametrize("test_data, expected", [
    ([['C'], ['M'], ['Z', 'N', 'D', 'P']], 'CMZ'),
    ([['M'], ['C'], ['D', 'N', 'Z', 'P']], 'MCD')
])
def test_get_tops(test_data, expected):
    data = get_tops(test_data)
    assert data == expected
