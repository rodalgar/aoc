import operator

import pytest

from Main import parse_input, Operation, check_operation, part1, concat_numbers, part2

test_raw_data = [
    '190: 10 19',
    '3267: 81 40 27',
    '83: 17 5',
    '156: 15 6',
    '7290: 6 8 6 15',
    '161011: 16 10 13',
    '192: 17 8 14',
    '21037: 9 7 18 13',
    '292: 11 6 16 20'
]


def get_test_data():
    return [Operation(test_value=190, numbers=[10, 19]),
            Operation(test_value=3267, numbers=[81, 40, 27]),
            Operation(test_value=83, numbers=[17, 5]),
            Operation(test_value=156, numbers=[15, 6]),
            Operation(test_value=7290, numbers=[6, 8, 6, 15]),
            Operation(test_value=161011, numbers=[16, 10, 13]),
            Operation(test_value=192, numbers=[17, 8, 14]),
            Operation(test_value=21037, numbers=[9, 7, 18, 13]),
            Operation(test_value=292, numbers=[11, 6, 16, 20])]


def get_operators_part1():
    return [operator.mul, operator.add]


def get_operators_part2():
    return [operator.mul, operator.add, concat_numbers]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == get_test_data()


@pytest.mark.parametrize("operation,operators,expected_result", [
    (get_test_data()[0], get_operators_part1(), True),
    (get_test_data()[1], get_operators_part1(), True),
    (get_test_data()[2], get_operators_part1(), False),
    (get_test_data()[3], get_operators_part1(), False),
    (get_test_data()[4], get_operators_part1(), False),
    (get_test_data()[5], get_operators_part1(), False),
    (get_test_data()[6], get_operators_part1(), False),
    (get_test_data()[7], get_operators_part1(), False),
    (get_test_data()[8], get_operators_part1(), True),
    (get_test_data()[0], get_operators_part2(), True),
    (get_test_data()[1], get_operators_part2(), True),
    (get_test_data()[2], get_operators_part2(), False),
    (get_test_data()[3], get_operators_part2(), True),
    (get_test_data()[4], get_operators_part2(), True),
    (get_test_data()[5], get_operators_part2(), False),
    (get_test_data()[6], get_operators_part2(), True),
    (get_test_data()[7], get_operators_part2(), False),
    (get_test_data()[8], get_operators_part2(), True),
])
def test_check_operation(operation, operators, expected_result):
    data = check_operation(operation, operators)
    assert data == expected_result


def test_part1():
    data = part1(get_test_data())
    assert data == 3749


@pytest.mark.parametrize("number_a, number_b, expected", [
    (1, 2, 12),
    (15, 6, 156),
    (12, 345, 12345)
])
def test_concat_numbers(number_a, number_b, expected):
    data = concat_numbers(number_a, number_b)
    assert data == expected


def test_part2():
    data = part2(get_test_data())
    assert data == 11387
