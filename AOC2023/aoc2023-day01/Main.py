# Day 1: Trebuchet?!
from typing import List, Optional, Dict

numbers = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}


# PART 1
def get_numbers_from_line(line: str) -> int:
    left = None
    right = None
    limit = len(line)
    for i in range(0, limit):
        if line[i].isdigit():
            left = int(line[i])
            break
    for i in range(limit - 1, -1, -1):
        if line[i].isdigit():
            right = int(line[i])
            break
    return left * 10 + right


def part1(data: List[str]) -> int:
    return sum([get_numbers_from_line(line) for line in data])


# PART 2
def extract_number(line: str, index: int, patterns: Dict[str, int]) -> Optional[int]:
    for k, v in patterns.items():
        len_pattern = len(k)
        if index + len_pattern > len(line):
            continue
        if k == line[index:index + len_pattern]:
            return v
    return None


def get_numbers_from_line_v2(line: str) -> int:
    left = None
    right = None
    limit = len(line)
    for i in range(0, limit):
        if line[i].isdigit():
            left = int(line[i])
            break
        else:
            number = extract_number(line, i, numbers)
            if number is not None:
                left = number
                break
    rev_numbers = {k[::-1]: v for k, v in numbers.items()}
    rev_line = line[::-1]
    for i in range(0, limit):
        if rev_line[i].isdigit():
            right = int(rev_line[i])
            break
        else:
            number = extract_number(rev_line, i, rev_numbers)
            if number is not None:
                right = number
                break
    return left * 10 + right


def part2(data: List[str]) -> int:
    return sum([get_numbers_from_line_v2(line) for line in data])


if __name__ == '__main__':
    with open('data/aoc2023-input-day01.txt', 'r') as f:
        raw_data = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    print('>>>SOLUTION: ', part1(raw_data))

    print('PART 2')
    print('>>>SOLUTION: ', part2(raw_data))
