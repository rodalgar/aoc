# Day 9: Smoke Basin
import operator
from functools import reduce
from typing import List, Tuple


def parse_input(raw_data: List[str]) -> List[List[int]]:
    return [list(map(int, line)) for line in raw_data]


def search_minimums(data: List[List[int]]) -> List[Tuple[int, int, int]]:
    minimums = []
    for row in range(len(data)):
        for col in range(len(data[0])):
            if row > 0:
                # top
                if data[row - 1][col] <= data[row][col]:
                    continue
            if col > 0:
                # to the left
                if data[row][col - 1] <= data[row][col]:
                    continue
            if row < (len(data) - 1):
                # bottom
                if data[row + 1][col] <= data[row][col]:
                    continue
            if col < (len(data[0]) - 1):
                # to the right
                if data[row][col + 1] <= data[row][col]:
                    continue
            minimums.append((row, col, data[row][col]))
    return minimums


def calculate_risks(minimums: List[Tuple[int, int, int]]) -> int:
    return sum(x + 1 for _, _, x in minimums)


def get_basin_from(data: List[List[int]], starting_row: int, starting_col: int) -> List[Tuple[int, int]]:
    to_visit = [(starting_row, starting_col)]
    basin = []

    while len(to_visit) > 0:
        step_row, step_col = to_visit[0]
        to_visit = to_visit[1:]
        # mark as visited
        basin.append((step_row, step_col))
        # try to add adjacent positions
        if step_row > 0:
            # top
            next_step = (step_row - 1, step_col)
            if data[next_step[0]][next_step[1]] < 9 and next_step not in to_visit and next_step not in basin:
                to_visit.append(next_step)
        if step_col > 0:
            # to the left
            next_step = (step_row, step_col - 1)
            if data[next_step[0]][next_step[1]] < 9 and next_step not in to_visit and next_step not in basin:
                to_visit.append(next_step)
        if step_row < (len(data) - 1):
            # bottom
            next_step = (step_row + 1, step_col)
            if data[next_step[0]][next_step[1]] < 9 and next_step not in to_visit and next_step not in basin:
                to_visit.append(next_step)
        if step_col < (len(data[0]) - 1):
            # to the right
            next_step = (step_row, step_col + 1)
            if data[next_step[0]][next_step[1]] < 9 and next_step not in to_visit and next_step not in basin:
                to_visit.append(next_step)

    return basin


def get_largest_basins(data: List[List[int]], minimums: List[Tuple[int, int, int]]):
    return reduce(operator.mul, sorted([len(get_basin_from(data, x, y)) for x, y, z in minimums], reverse=True)[:3])


if __name__ == '__main__':
    with open('data/aoc2021-input-day09.txt', 'r') as f:
        sol_raw_map = [line.strip('\n') for line in f.readlines()]

    # PART 1
    sol_data = parse_input(sol_raw_map)
    sol_minimums = search_minimums(sol_data)
    print('PART 1')
    print('>>>SOLUTION: ', calculate_risks(sol_minimums))

    # PART 2
    print('PART 2')
    print('>>>SOLUTION:', get_largest_basins(sol_data, sol_minimums))
