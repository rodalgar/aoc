from __future__ import annotations
from typing import List
import re


class Board:
    rows = None
    marked = None
    row_size = None
    is_winner = None
    id = None

    def __init__(self, board_id: int):
        self.rows = []
        self.marked = []
        self.is_winner = self.check_is_winner()
        self.id = board_id

    def __repr__(self):
        return f"B{self.id}"

    @staticmethod
    def parse_board(numbers: List[str], board_id: int) -> Board:
        board = Board(board_id)
        size = None
        for line in numbers:
            line = re.sub('  ', ' ', line)
            line = re.sub('^ ', '', line)
            new_row = [int(x) for x in line.split(' ')]
            board.rows.append(new_row)
            board.marked.append([0 for _ in range(len(board.rows[0]))])
            size = len(new_row)

        board.row_size = size

        return board

    def print_board(self) -> None:
        print('Board ', self.id)
        print(25 * '-')
        for row in range(len(self.rows)):
            line = '| '
            for col in range(len(self.rows[row])):
                mark = 'X' if self.marked[row][col] == 1 else ' '
                line += f'{self.rows[row][col]:>3}{mark}'
            print(line + ' |')
        print(25 * '-')

    def mark_number(self, number: int) -> None:
        for i in range(len(self.rows)):
            for j in range(self.row_size):
                if self.rows[i][j] == number:
                    self.marked[i][j] = 1
        self.is_winner = self.check_is_winner()

    def check_is_winner(self) -> bool:
        # Any full rows?
        for i in range(len(self.rows)):
            if sum(self.marked[i]) == self.row_size:
                return True

        # Maybe any full column?
        for i in range(len(self.rows)):
            if sum([row[i] for row in self.marked]) == len(self.rows):
                return True

        return False

    def get_sum_unmarked(self):
        res = 0
        for i in range(len(self.rows)):
            for j in range(self.row_size):
                if not self.marked[i][j]:
                    res += self.rows[i][j]
        return res
