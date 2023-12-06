# Day 6: Wait For It
import math
import operator
from functools import reduce


# PART 1
def parse_input_part1(raw_data: list[str]) -> list[tuple[int, int]]:
    times = map(int, filter(lambda x: x != '', raw_data[0].split(':')[1].split(' ')))
    distances = map(int, filter(lambda x: x != '', raw_data[1].split(':')[1].split(' ')))

    return [(t, d) for t, d in zip(times, distances)]


# PART 2
def parse_input_part2(raw_data: list[str]) -> list[tuple[int, int]]:
    time = int(raw_data[0].split(':')[1].replace(' ', ''))
    distance = int(raw_data[1].split(':')[1].replace(' ', ''))

    return [(time, distance)]


# PART 1 & 2
def calculate(time: int, record: int) -> int:
    # formulae => y = a ( x - a ), space equals speed multiplied by time moving (total time minus time pressing button)
    # formulae => y = (- a ^2) + (time a) + (-record), for y = 0
    # Solution: roots = -b +- (sqrt ( b^2 - 4 a c ) / 2a)
    discriminator = math.sqrt((time ** 2) - 4 * (-1) * (- record))

    root_1 = (-time + discriminator) / (2 * (-1))
    root_2 = (-time - discriminator) / (2 * (-1))
    left = min(root_1, root_2)
    right = max(root_1, root_2)

    left_is_whole_number = math.ceil(left) - math.floor(left) == 1
    right_is_whole_number = math.ceil(right) - math.floor(right) == 1

    left_offset = 0 if left_is_whole_number else -1
    right_offset = 0 if right_is_whole_number else -1

    return math.floor(right) - math.ceil(left) + left_offset + right_offset + 1


def accrue_times(data: list[tuple[int, int]]) -> int:
    return reduce(operator.mul, (calculate(t, d) for t, d in data))


if __name__ == '__main__':
    with open('data/aoc2023-input-day06.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    print('>>>>SOLUTION: ', accrue_times(parse_input_part1(sol_raw_data)))

    print('PART 2')
    print('>>>>SOLUTION: ', accrue_times(parse_input_part2(sol_raw_data)))
