import pytest

from Main import (parse_input, get_hand_type, get_hand_type_jokers, calculate_winnings,
                  Hand_types, card_strength_with_jokers, card_strength_without_jokers)

test_raw_data = [
    '32T3K 765',
    'T55J5 684',
    'KK677 28',
    'KTJJT 220',
    'QQQJA 483'
]


def get_test_data():
    return [('32T3K', 765),
            ('T55J5', 684),
            ('KK677', 28),
            ('KTJJT', 220),
            ('QQQJA', 483)]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == [('32T3K', 765),
                    ('T55J5', 684),
                    ('KK677', 28),
                    ('KTJJT', 220),
                    ('QQQJA', 483)]


@pytest.mark.parametrize("hand, expected", [
    ('32T3K', Hand_types.ONE_PAIR),
    ('T55J5', Hand_types.THREE_OF_KIND),
    ('KK677', Hand_types.TWO_PAIR),
    ('KTJJT', Hand_types.TWO_PAIR),
    ('QQQJA', Hand_types.THREE_OF_KIND)
])
def test_get_hand_type(hand, expected):
    data = get_hand_type(hand)
    assert data == expected


@pytest.mark.parametrize("hand, expected", [
    ('32T3K', Hand_types.ONE_PAIR),
    ('T55J5', Hand_types.FOUR_OF_KIND),
    ('KK677', Hand_types.TWO_PAIR),
    ('KTJJT', Hand_types.FOUR_OF_KIND),
    ('QQQJA', Hand_types.FOUR_OF_KIND)
])
def test_get_hand_type_jokers(hand, expected):
    data = get_hand_type_jokers(hand)
    assert data == expected


def test_calculate_winnings_no_jokers():
    data = calculate_winnings(get_test_data(), card_strength_without_jokers, get_hand_type)
    assert data == 6440


def test_calculate_winnings_jokers():
    data = calculate_winnings(get_test_data(), card_strength_with_jokers, get_hand_type_jokers)
    assert data == 5905
