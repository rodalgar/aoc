# Day 11: Dumbo Octopus
from collections import deque
from typing import List


def parse_input(raw_data: List[str]) -> List[List[int]]:
    return [list(map(int, line)) for line in raw_data]


def print_map(the_map: List[List[int]]) -> None:
    for row in the_map:
        print(''.join(map(str, row)))


def key(row: int, col: int) -> str:
    return f"{row}-{col}"


# PART 1
def do_step(map_data: List[List[int]]) -> int:
    max_row = len(map_data)
    max_col = len(map_data[0])
    flashed = set()
    to_flash = deque()
    # natural increase
    for row in range(max_row):
        for col in range(max_col):
            map_data[row][col] += 1
            if map_data[row][col] > 9:
                to_flash.append((row, col))

    # are there flasheable octopuses?
    while len(to_flash) > 0:
        row, col = to_flash.pop()
        if key(row, col) in flashed:
            continue
        flashed.add(key(row, col))
        map_data[row][col] = 0
        for f_row in range(row - 1, row + 2):
            for f_col in range(col - 1, col + 2):
                if 0 <= f_row < max_row and 0 <= f_col < max_col and key(f_row, f_col) not in flashed:
                    map_data[f_row][f_col] += 1
                    if map_data[f_row][f_col] > 9:
                        to_flash.append((f_row, f_col))
    return len(flashed)


# PART 2
def get_synchronized_map(map_data: List[List[int]]) -> int:
    cnt = 0
    while True:
        n_flash = do_step(map_data)
        cnt += 1
        if n_flash == 100:
            break
    return cnt


if __name__ == '__main__':
    with open('data/aoc2021-input-day11.txt', 'r') as f:
        sol_raw_map = [line.strip('\n') for line in f.readlines()]

    # PART 1
    sol_map = parse_input(sol_raw_map)
    octo_flashes = []
    for i in range(100):
        octo_flashes.append(do_step(sol_map))
    print('PART 1')
    print('>>>SOLUTION:', sum(octo_flashes))

    # PART 2
    print('PART 2')
    print('>>>SOLUTION:', get_synchronized_map(parse_input(sol_raw_map)))
