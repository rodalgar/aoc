# Day 1: Historian Hysteria
import operator
from collections import Counter
from functools import reduce


def parse_input(raw_data: [str]) -> [str]:
    left_part = []
    right_part = []
    for line in raw_data:
        chunks = line.split()
        left_part.append(int(chunks[0]))
        right_part.append(int(chunks[1]))
    return left_part, right_part


# PART 1
def get_distance(left_list: [int], right_list: [int]) -> int:
    return reduce(operator.add, [abs(l - r) for (l, r) in zip(sorted(left_list), sorted(right_list))])


# PART 2
def get_similarity_score(left_list: [int], right_list: [int]) -> int:
    count = Counter(right_list)
    return reduce(operator.add, [left_data * count[left_data] for left_data in left_list])


if __name__ == '__main__':
    with open('data/aoc2024-input-day01.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_left, sol_right = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', get_distance(sol_left, sol_right))

    print('PART 2')
    print('>>>>SOLUTION: ', get_similarity_score(sol_left, sol_right))
