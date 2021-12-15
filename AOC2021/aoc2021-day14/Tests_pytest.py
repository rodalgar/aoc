import pytest

from Main import parse_input, apply_steps_rec_v3

raw_test_data = [
    'NNCB',
    '',
    'CH -> B',
    'HH -> N',
    'CB -> H',
    'NH -> C',
    'HB -> C',
    'HC -> B',
    'HN -> C',
    'NN -> C',
    'BH -> H',
    'NC -> B',
    'NB -> B',
    'BN -> B',
    'BB -> N',
    'BC -> B',
    'CC -> N',
    'CN -> C'
]


def get_test_data():
    return ('NNCB',
            {'BB': 'N',
             'BC': 'B',
             'BH': 'H',
             'BN': 'B',
             'CB': 'H',
             'CC': 'N',
             'CH': 'B',
             'CN': 'C',
             'HB': 'C',
             'HC': 'B',
             'HH': 'N',
             'HN': 'C',
             'NB': 'B',
             'NC': 'B',
             'NH': 'C',
             'NN': 'C'})


def test_parse_input():
    data = parse_input(raw_test_data)
    assert data == ('NNCB',
                    {'BB': 'N',
                     'BC': 'B',
                     'BH': 'H',
                     'BN': 'B',
                     'CB': 'H',
                     'CC': 'N',
                     'CH': 'B',
                     'CN': 'C',
                     'HB': 'C',
                     'HC': 'B',
                     'HH': 'N',
                     'HN': 'C',
                     'NB': 'B',
                     'NC': 'B',
                     'NH': 'C',
                     'NN': 'C'})

@pytest.mark.parametrize("test_data,steps,expected",[
    (get_test_data(), 10, 1588),
    (get_test_data(), 40, 2188189693529),
])
def test_apply_steps_rec_v3(test_data, steps, expected):
    test_template, test_rules = get_test_data()
    data = apply_steps_rec_v3(test_template, test_rules, steps)
    assert data == expected
