import pytest
from Main import get_gamma_epsilon_rates, get_common_bits_at, get_life_support_rates

test_data = [
    '00100',
    '11110',
    '10110',
    '10111',
    '10101',
    '01111',
    '00111',
    '11100',
    '10000',
    '11001',
    '00010',
    '01010'
]


# PART 1
@pytest.mark.parametrize("position,expected_most,expected_least",
                         [(0, '1', '0'), (1, '0', '1'), (2, '1', '0'),
                          (3, '1', '0'), (4, '0', '1')])
def test_get_common_bits_at(position, expected_most, expected_least):
    most_common_bit, least_common_bit = get_common_bits_at(test_data, position)
    assert most_common_bit == expected_most
    assert least_common_bit == expected_least


def test_get_gamma_epsilon_rates():
    gamma_rate, epsilon_rate = get_gamma_epsilon_rates(test_data)
    assert gamma_rate == 22
    assert epsilon_rate == 9


# PART 2
def test_get_life_support_rates():
    oxygen_rate, co2_rate = get_life_support_rates(test_data)
    assert oxygen_rate == 23, 'wrong oxygen rate'
    assert co2_rate == 10, 'wrong co2 rate'
