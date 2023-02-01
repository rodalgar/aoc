from Main import parse_input, get_group_badges, get_misplaced_item

test_data_raw = [
    'vJrwpWtwJgWrhcsFMMfFFhFp',
    'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
    'PmmdzqPrVvPwwTWBwg',
    'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
    'ttgJtRGJQctTZtZT',
    'CrZsJsPPZsGzwwsLwLmpwMDw'
]


def get_test_data():
    return [['vJrwpWtwJgWr', 'hcsFMMfFFhFp', 'vJrwpWtwJgWrhcsFMMfFFhFp'],
            ['jqHRNqRjqzjGDLGL', 'rsFMfFZSrLrFZsSL', 'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL'],
            ['PmmdzqPrV', 'vPwwTWBwg', 'PmmdzqPrVvPwwTWBwg'],
            ['wMqvLMZHhHMvwLH', 'jbvcjnnSBnvTQFn', 'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn'],
            ['ttgJtRGJ', 'QctTZtZT', 'ttgJtRGJQctTZtZT'],
            ['CrZsJsPPZsGz', 'wwsLwLmpwMDw', 'CrZsJsPPZsGzwwsLwLmpwMDw']]


def test_parse_input():
    data = parse_input(test_data_raw)
    assert data == get_test_data()


def test_get_misplaced_item():
    data = get_misplaced_item(get_test_data())
    assert data == [16, 38, 42, 22, 20, 19]


def test_get_group_badges():
    data = get_group_badges(get_test_data())
    assert data == [18, 52]
