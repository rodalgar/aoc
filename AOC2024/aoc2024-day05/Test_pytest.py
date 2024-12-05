import pytest

from Main import parse_input, check_correct_update, get_correct_updates, part1, get_incorrect_updates, fix_update, part2

test_raw_data = [
    '47|53',
    '97|13',
    '97|61',
    '97|47',
    '75|29',
    '61|13',
    '75|53',
    '29|13',
    '97|29',
    '53|29',
    '61|53',
    '97|53',
    '61|29',
    '47|13',
    '75|47',
    '97|75',
    '47|61',
    '75|61',
    '47|29',
    '75|13',
    '53|13',
    '',
    '75,47,61,53,29',
    '97,61,53,29,13',
    '75,29,13',
    '75,97,47,61,53',
    '61,13,29',
    '97,13,75,29,47',
]


def get_test_data():
    return ({13: set(),
             29: {13},
             47: {29, 13, 61, 53},
             53: {13, 29},
             61: {29, 53, 13},
             75: {13, 47, 29, 53, 61},
             97: {75, 13, 47, 61, 53, 29}},
            [[75, 47, 61, 53, 29],
             [97, 61, 53, 29, 13],
             [75, 29, 13],
             [75, 97, 47, 61, 53],
             [61, 13, 29],
             [97, 13, 75, 29, 47]])


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == get_test_data()


@pytest.mark.parametrize("rules, update, expected", [
    (get_test_data()[0], get_test_data()[1][0], True),
    (get_test_data()[0], get_test_data()[1][1], True),
    (get_test_data()[0], get_test_data()[1][2], True),
    (get_test_data()[0], get_test_data()[1][3], False),
    (get_test_data()[0], get_test_data()[1][4], False),
    (get_test_data()[0], get_test_data()[1][5], False)
])
def test_check_correct_update(rules, update, expected):
    data = check_correct_update(rules, update)
    assert data == expected


def test_get_correct_updates():
    data = get_correct_updates(*get_test_data())
    assert data == get_test_data()[1][:3]


def test_part1():
    data = part1(*get_test_data())
    assert data == 143


def test_get_incorrect_updates():
    data = get_incorrect_updates(*get_test_data())
    assert data == get_test_data()[1][3:]


@pytest.mark.parametrize("bad_update,expected", [
    (get_test_data()[1][3], [97, 75, 47, 61, 53]),
    (get_test_data()[1][4], [61, 29, 13]),
    (get_test_data()[1][5], [97, 75, 47, 29, 13]),
])
def test_fix_update(bad_update, expected):
    data = fix_update(get_test_data()[0], bad_update)
    assert data == expected


def test_part2():
    data = part2(*get_test_data())
    assert data == 123
