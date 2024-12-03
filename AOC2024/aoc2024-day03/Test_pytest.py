import pytest

from Main import part1, part2

test_raw_data_1 = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
test_raw_data_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def test_part1():
    data = part1([test_raw_data_1])
    assert data == 161


def test_part2():
    data = part2([test_raw_data_2])
    assert data == 48
