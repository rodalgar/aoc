import operator
import pytest
from functools import reduce

from Main import Monkey, Operation, parse_input, get_active_monkeys, calculate_new_worry_p1, calculate_new_worry_p2, \
    is_divisible_p1, is_divisible_p2, convert_monkeys

test_raw_data = [
    'Monkey 0:',
    '  Starting items: 79, 98',
    '  Operation: new = old * 19',
    '  Test: divisible by 23',
    '    If true: throw to monkey 2',
    '    If false: throw to monkey 3',
    '',
    'Monkey 1:',
    '  Starting items: 54, 65, 75, 74',
    '  Operation: new = old + 6',
    '  Test: divisible by 19',
    '    If true: throw to monkey 2',
    '    If false: throw to monkey 0',
    '',
    'Monkey 2:',
    '  Starting items: 79, 60, 97',
    '  Operation: new = old * old',
    '  Test: divisible by 13',
    '    If true: throw to monkey 1',
    '    If false: throw to monkey 3',
    '',
    'Monkey 3:',
    '  Starting items: 74',
    '  Operation: new = old + 3',
    '  Test: divisible by 17',
    '    If true: throw to monkey 0',
    '    If false: throw to monkey 1'
]


def get_test_data():
    return [Monkey(id=0, items=[79, 98], operation_fun=Operation(left_side='old', operator='*', right_side='19'),
                   divisible_by=23, test_true=2, test_false=3),
            Monkey(id=1, items=[54, 65, 75, 74], operation_fun=Operation(left_side='old', operator='+', right_side='6'),
                   divisible_by=19, test_true=2, test_false=0),
            Monkey(id=2, items=[79, 60, 97], operation_fun=Operation(left_side='old', operator='*', right_side='old'),
                   divisible_by=13, test_true=1, test_false=3),
            Monkey(id=3, items=[74], operation_fun=Operation(left_side='old', operator='+', right_side='3'),
                   divisible_by=17, test_true=0, test_false=1)]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == get_test_data()


@pytest.mark.parametrize("turns, worry_fun, div_fun, relief, expected", [
    (20, calculate_new_worry_p1, is_divisible_p1, True, 10605),
    (20, calculate_new_worry_p1, is_divisible_p1, False, 10197),
])
def test_get_active_monkeys_part1(turns, worry_fun, div_fun, relief, expected):
    data = get_active_monkeys(get_test_data(), turns, worry_fun, div_fun, relief, 2, False)
    data = reduce(operator.mul, (d[1] for d in data))
    assert data == expected


@pytest.mark.parametrize("turns, worry_fun, div_fun, relief, expected", [
    (1, calculate_new_worry_p2, is_divisible_p2, False, 24),
    (20, calculate_new_worry_p2, is_divisible_p2, False, 10197),
    (1000, calculate_new_worry_p2, is_divisible_p2, False, 27019168),
    (2000, calculate_new_worry_p2, is_divisible_p2, False, 108263829),
    (3000, calculate_new_worry_p2, is_divisible_p2, False, 243843334),
    (4000, calculate_new_worry_p2, is_divisible_p2, False, 433783826),
    (5000, calculate_new_worry_p2, is_divisible_p2, False, 677950000),
    (10000, calculate_new_worry_p2, is_divisible_p2, False, 2713310158),
])
def test_get_active_monkeys_part2(turns, worry_fun, div_fun, relief, expected):
    data = convert_monkeys(get_test_data())
    data = get_active_monkeys(data, turns, worry_fun, div_fun, relief, 2, False)
    data = reduce(operator.mul, (d[1] for d in data))
    assert data == expected
