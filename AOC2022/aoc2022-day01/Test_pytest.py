import pytest

from Main import parse_input, get_top_calorie_elves

test_raw_data = [
    '1000',
    '2000',
    '3000',
    '',
    '4000',
    '',
    '5000',
    '6000',
    '',
    '7000',
    '8000',
    '9000',
    '',
    '10000',
    ''
]


def get_test_data():
    return [(6000, [1000, 2000, 3000]),
            (4000, [4000]),
            (11000, [5000, 6000]),
            (24000, [7000, 8000, 9000]),
            (10000, [10000])
            ]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == get_test_data()


@pytest.mark.parametrize("number_of_elves, expected", [(1, 24000), (3, 45000)])
def test_get_top_calorie_elves(number_of_elves, expected):
    data = get_top_calorie_elves(get_test_data(), number_of_elves)
    assert data == expected
