from Board import Board
from Main import parse, play_first_win, play_last_win, index_boards_per_number


def get_test_input():
    test_input = [
        '7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1',
        '',
        '22 13 17 11  0',
        ' 8  2 23  4 24',
        '21  9 14 16  7',
        ' 6 10  3 18  5',
        ' 1 12 20 15 19',
        '',
        ' 3 15  0  2 22',
        ' 9 18 13 17  5',
        '19  8  7 25 23',
        '20 11 10 24  4',
        '14 21 16 12  6',
        '',
        '14 21 17 24  4',
        '10 16 15  9 19',
        '18  8 23 26 20',
        '22 11 13  6  5',
        ' 2  0 12  3  7',
    ]
    return test_input


def get_test_boards():
    boards = [Board(1), Board(2), Board(3)]
    boards[0].rows = [[22, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7],
                      [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]]
    boards[1].rows = [[3, 15, 0, 2, 22], [9, 18, 13, 17, 5], [19, 8, 7, 25, 23],
                      [20, 11, 10, 24, 4], [14, 21, 16, 12, 6]]
    boards[2].rows = [[14, 21, 17, 24, 4], [10, 16, 15, 9, 19], [18, 8, 23, 26, 20],
                      [22, 11, 13, 6, 5], [2, 0, 12, 3, 7]]
    for b in boards:
        b.marked = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        b.row_size = 5
    return boards


def get_test_drawn_numbers():
    return [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1]


def get_index_boards_per_number():
    boards = get_test_boards()
    b1 = boards[0]
    b2 = boards[1]
    b3 = boards[2]

    return {22: [b1, b2, b3], 13: [b1, b2, b3], 17: [b1, b2, b3], 11: [b1, b2, b3], 0: [b1, b2, b3], 8: [b1, b2, b3],
            2: [b1, b2, b3], 23: [b1, b2, b3], 4: [b1, b2, b3], 24: [b1, b2, b3], 21: [b1, b2, b3], 9: [b1, b2, b3],
            14: [b1, b2, b3], 16: [b1, b2, b3], 7: [b1, b2, b3], 6: [b1, b2, b3], 10: [b1, b2, b3], 3: [b1, b2, b3],
            18: [b1, b2, b3], 5: [b1, b2, b3], 1: [b1], 12: [b1, b2, b3], 20: [b1, b2, b3], 15: [b1, b2, b3],
            19: [b1, b2, b3],
            25: [b2], 26: [b3]}


def test_parse():
    numbers, boards = parse(get_test_input())
    expected_numbers = get_test_drawn_numbers()

    assert numbers == expected_numbers
    assert len(boards) == 3


def test_play_first_win():
    numbers = get_test_drawn_numbers()
    boards = get_test_boards()

    value, last_number = play_first_win(boards, numbers)
    result = value * last_number
    assert value == 188
    assert last_number == 24
    assert result == 4512


def test_play_last_win():
    numbers = get_test_drawn_numbers()
    boards = get_test_boards()

    value, last_number = play_last_win(boards, numbers)
    result = value * last_number
    assert value == 148
    assert last_number == 13
    assert result == 1924


def test_index_boards_per_number():
    boards = get_test_boards()
    indexed = index_boards_per_number(boards)
    expected_indexes = get_index_boards_per_number()

    assert indexed.keys() == expected_indexes.keys()
    for k in expected_indexes.keys():
        rep_values = [b.__repr__() for b in indexed[k]]
        expected_values = [b.__repr__() for b in expected_indexes[k]]
        assert rep_values == expected_values
