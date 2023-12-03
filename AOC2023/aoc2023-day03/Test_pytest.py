import pytest

from Main import parse_input, divide_parts, part1, part2, Number, Symbol

test_raw_data = [
    '467..114..',
    '...*......',
    '..35..633.',
    '......#...',
    '617*......',
    '.....+.58.',
    '..592.....',
    '......755.',
    '...$.*....',
    '.664.598..'
]


def get_test_data():
    return ([Number(value=467, left=0, right=2, line=0),
             Number(value=114, left=5, right=7, line=0),
             Number(value=35, left=2, right=3, line=2),
             Number(value=633, left=6, right=8, line=2),
             Number(value=617, left=0, right=2, line=4),
             Number(value=58, left=7, right=8, line=5),
             Number(value=592, left=2, right=4, line=6),
             Number(value=755, left=6, right=8, line=7),
             Number(value=664, left=1, right=3, line=9),
             Number(value=598, left=5, right=7, line=9)],
            [Symbol(id_symbol=1, glyph='*', pos=3, line=1),
             Symbol(id_symbol=2, glyph='#', pos=6, line=3),
             Symbol(id_symbol=3, glyph='*', pos=3, line=4),
             Symbol(id_symbol=4, glyph='+', pos=5, line=5),
             Symbol(id_symbol=5, glyph='$', pos=3, line=8),
             Symbol(id_symbol=6, glyph='*', pos=5, line=8)])


def get_test_numbers():
    return get_test_data()[0]


def get_test_symbols():
    return get_test_data()[1]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == get_test_data()


def test_divide_parts():
    part_numbers, other_numbers, gears = divide_parts(get_test_numbers(), get_test_symbols())
    assert part_numbers == [Number(value=467, left=0, right=2, line=0),
                            Number(value=35, left=2, right=3, line=2),
                            Number(value=633, left=6, right=8, line=2),
                            Number(value=617, left=0, right=2, line=4),
                            Number(value=592, left=2, right=4, line=6),
                            Number(value=755, left=6, right=8, line=7),
                            Number(value=664, left=1, right=3, line=9),
                            Number(value=598, left=5, right=7, line=9)]
    assert other_numbers == [Number(value=114, left=5, right=7, line=0),
                             Number(value=58, left=7, right=8, line=5)]
    assert gears == [Symbol(id_symbol=1, glyph='*', pos=3, line=1, numbers=[467, 35]),
                     Symbol(id_symbol=6, glyph='*', pos=5, line=8, numbers=[755, 598])]


def test_part1():
    data = part1([Number(value=467, left=0, right=2, line=0),
                  Number(value=35, left=2, right=3, line=2),
                  Number(value=633, left=6, right=8, line=2),
                  Number(value=617, left=0, right=2, line=4),
                  Number(value=592, left=2, right=4, line=6),
                  Number(value=755, left=6, right=8, line=7),
                  Number(value=664, left=1, right=3, line=9),
                  Number(value=598, left=5, right=7, line=9)])
    assert data == 4361


def test_part2():
    data = part2([Symbol(id_symbol=1, glyph='*', pos=3, line=1, numbers=[467, 35]),
                  Symbol(id_symbol=6, glyph='*', pos=5, line=8, numbers=[755, 598])])
    assert data == 467835
