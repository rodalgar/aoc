import pytest

from Main import parse_input, blink_compact, blink_compact_init

test_raw_data_1 = '0 1 10 99 999'
test_raw_data_2 = '125 17'


def get_test_data_1():
    return ['0', '1', '10', '99', '999']


def get_test_data_2():
    return ['125', '17']


@pytest.mark.parametrize("test_data, expected", [
    (test_raw_data_1, get_test_data_1()),
    (test_raw_data_2, get_test_data_2())
])
def test_parse_input(test_data, expected):
    data = parse_input(test_data)
    assert data == expected


def test_blink_compact():
    data = blink_compact({'0': 1, '1': 1, '10': 1, '99': 1, '999': 1})
    assert data == {'1': 2, '2024': 1, '0': 1, '9': 2, '2021976': 1}


@pytest.mark.parametrize("test_data, iterations, expected", [
    (get_test_data_2(), 1, 3),
    (get_test_data_2(), 2, 4),
    (get_test_data_2(), 3, 5),
    (get_test_data_2(), 4, 9),
    (get_test_data_2(), 5, 13),
    (get_test_data_2(), 6, 22),
    (get_test_data_2(), 25, 55312)
])
def test_blink_compact_init(test_data, iterations, expected):
    _, num_elements = blink_compact_init(test_data, iterations)
    assert num_elements == expected
