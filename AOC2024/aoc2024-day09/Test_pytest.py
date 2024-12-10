import pytest

from Main import parse_input, defragment_by_block, calculate_checksum, defragment_by_file

test_small_raw_data = '12345'
test_raw_data = '2333133121414131402'


def get_test_data_small_1():
    return ['0', '.', '.', '1', '1', '1', '.', '.', '.', '.', '2', '2', '2', '2', '2']


def get_test_data_1():
    return ['0', '0', '.', '.', '.', '1', '1', '1', '.', '.', '.', '2', '.', '.', '.', '3', '3', '3', '.', '4', '4',
            '.', '5', '5', '5', '5', '.', '6', '6', '6', '6', '.', '7', '7', '7', '.', '8', '8', '8', '8', '9', '9']


def get_defragment_by_block_small_1():
    return ['0', '2', '2', '1', '1', '1', '2', '2', '2', '.', '.', '.', '.', '.', '.']


def get_defragment_by_block_1():
    return ['0', '0', '9', '9', '8', '1', '1', '1', '8', '8', '8', '2', '7', '7', '7', '3', '3', '3', '6', '4', '4',
            '6', '5', '5', '5', '5', '6', '6', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']


def get_defragment_by_file_small_1():
    return ['0', '.', '.', '1', '1', '1', '.', '.', '.', '.', '2', '2', '2', '2', '2']


def get_defragment_by_file_1():
    return ['0', '0', '9', '9', '2', '1', '1', '1', '7', '7', '7', '.', '4', '4', '.', '3', '3', '3', '.', '.', '.',
            '.', '5', '5', '5', '5', '.', '6', '6', '6', '6', '.', '.', '.', '.', '.', '8', '8', '8', '8', '.', '.']


@pytest.mark.parametrize("raw_data, expected", [
    (test_small_raw_data, get_test_data_small_1()),
    (test_raw_data, get_test_data_1())
])
def test_parse_input(raw_data, expected):
    data = parse_input(raw_data)
    assert data == expected


@pytest.mark.parametrize("test_data, expected", [
    (get_test_data_small_1(), get_defragment_by_block_small_1()),
    (get_test_data_1(), get_defragment_by_block_1())
])
def test_defragment_by_block(test_data, expected):
    data = defragment_by_block(test_data)
    assert data == expected


@pytest.mark.parametrize("test_data, expected", [
    (get_test_data_small_1(), get_defragment_by_file_small_1()),
    (get_test_data_1(), get_defragment_by_file_1())
])
def test_defragment_by_file(test_data, expected):
    data = defragment_by_file(test_data)
    assert data == expected


@pytest.mark.parametrize("test_data, expected", [
    (get_defragment_by_block_1(), 1928),
    (get_defragment_by_file_1(), 2858)
])
def test_calculate_checksum(test_data, expected):
    data = calculate_checksum(test_data)
    assert data == expected
