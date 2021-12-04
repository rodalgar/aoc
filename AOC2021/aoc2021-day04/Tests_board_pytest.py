from Board import Board


def get_test_board() -> Board:
    board = Board(1)
    board.rows = [[22, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7],
                      [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]]
    board.marked = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    board.row_size = 5
    return board


def test_parse_board():
    test_input = ['22 59  7 10  6', '33 36 96 55 23', '13 85 18 29 28', '75 46 83 73 58', '34 40 87 56 98']
    board_id = 1
    board = Board.parse_board(test_input, board_id)

    assert board.id == board_id
    assert board.rows == [[22, 59, 7, 10, 6], [33, 36, 96, 55, 23], [13, 85, 18, 29, 28],
                          [75, 46, 83, 73, 58], [34, 40, 87, 56, 98]]
    assert board.marked == [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]


def test_mark_number():
    board = get_test_board()
    board.mark_number(23)

    assert board.marked == [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]


def test_get_sum_unmarked():
    board = get_test_board()
    board.marked = [[1, 1, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1]]

    value = board.get_sum_unmarked()
    assert value == 200
