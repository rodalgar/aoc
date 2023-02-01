# Day 1: Calorie Counting
from typing import List, Tuple


def parse_input(raw_calories: List[str]) -> List[Tuple[int, List[int]]]:
    elves = []
    elf_calories = []
    elf_total_calories = 0
    parsing_elf = False
    for cal in raw_calories:
        parsing_elf = True
        if len(cal) > 0:
            cal = int(cal)
            elf_calories.append(cal)
            elf_total_calories += cal
        else:
            elves.append((elf_total_calories, elf_calories))
            elf_calories = []
            elf_total_calories = 0
            parsing_elf = False
    if parsing_elf:
        elves.append((elf_total_calories, elf_calories))

    return elves


# PART 1 & PART 2
def get_top_calorie_elves(elves: List[Tuple[int, List[int]]], number_top_elves: int) -> int:
    calories = [total for total, _ in elves]
    calories.sort(reverse=True)
    return sum(calories[:number_top_elves])


if __name__ == '__main__':
    with open('data/aoc2022-input-day01.txt', 'r') as f:
        raw_data = [line.strip('\n') for line in f.readlines()]

    data = parse_input(raw_data)

    print('PART 1')
    print('>>>SOLUTION: ', get_top_calorie_elves(data, number_top_elves=1))

    print('PART 2')
    print('>>>SOLUTION: ', get_top_calorie_elves(data, number_top_elves=3))
