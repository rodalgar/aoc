# Day 4: Giant Squid
from collections import defaultdict
from copy import deepcopy
from typing import List, Tuple, Dict
from Board import Board


def parse(raw_input: List[str]) -> Tuple[List[int], List[Board]]:
    drawn_numbers = [int(x) for x in raw_input[0].split(',')]
    n_line = 2
    boards = []
    while n_line < len(raw_input):
        board = Board.parse_board(raw_input[n_line:n_line + 5], len(boards) + 1)
        n_line += 6
        boards.append(board)
    return drawn_numbers, boards


def index_boards_per_number(boards: List[Board]) -> Dict[int, List[Board]]:
    indexed_boards_by_numbers = defaultdict(list)
    for b in boards:
        for row in b.rows:
            for n in row:
                indexed_boards_by_numbers[n].append(b)
    return indexed_boards_by_numbers


# PART 1
def play_first_win(boards_in: List[Board], drawn_numbers: List[int]) -> Tuple[int, int]:
    # index boards
    # for each drawn number...
    #  ... look for boards containing the number (indexed!)
    #  ... play_first_win turn
    #  ... stop if any winners
    # calculate points on winner board
    boards = deepcopy(boards_in)
    indexed_boards_by_numbers = index_boards_per_number(boards)

    for n in drawn_numbers:
        for b in indexed_boards_by_numbers[n]:
            b.mark_number(n)
            if b.is_winner:
                return b.get_sum_unmarked(), n


# PART 2
def play_last_win(boards_in: List[Board], drawn_numbers: List[int]) -> Tuple[int, int]:
    boards = deepcopy(boards_in)
    remaining_boards = boards[:]
    indexed_boards_by_numbers = index_boards_per_number(boards)

    for n in drawn_numbers:
        for b in indexed_boards_by_numbers[n]:
            if b.is_winner:
                continue

            b.mark_number(n)
            if b.is_winner:
                if len(remaining_boards) == 1:
                    return remaining_boards[0].get_sum_unmarked(), n
                remaining_boards.remove(b)


if __name__ == '__main__':
    with open('data/aoc2021-input-day04.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_list_numbers, sol_list_boards = parse(sol_raw_data)

    # PART 1
    result, last_number_played = play_first_win(sol_list_boards, sol_list_numbers)
    print('PART 1')
    print(">>>SOLUTION: ", result * last_number_played)

    # PART 2
    result, last_number_played = play_last_win(sol_list_boards, sol_list_numbers)
    print('PART 2')
    print(">>>SOLUTION: ", result * last_number_played)
