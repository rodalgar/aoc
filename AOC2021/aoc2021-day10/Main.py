# Day 10: Syntax Scoring
from collections import deque
from enum import Enum
from functools import reduce
from typing import List, Tuple, Optional, Any

matching_pairs = {
    '[': ']',
    '(': ')',
    '{': '}',
    '<': '>'
}

error_score = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

incomplete_score = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


# PART 1
class ValidationResult(Enum):
    OK = 1
    CORRUPTED = 2
    INCOMPLETE = 3


def check_line(line: str) -> Tuple[ValidationResult, Optional[Any], int]:
    stack = deque()
    for i in range(len(line)):
        symbol = line[i]
        if symbol in matching_pairs:
            # opening chunk we stack it's closing pair
            stack.append(matching_pairs[symbol])
        else:
            # closing chunk, must match stacked symbol
            stacked = stack.pop()
            if stacked != symbol:
                return ValidationResult.CORRUPTED, i, error_score[symbol]
    if len(stack) > 0:
        return ValidationResult.INCOMPLETE, stack, 0
    return ValidationResult.OK, None, 0


def process_lines(lines: List[str]) -> List[ValidationResult]:
    return list(map(check_line, lines))


def calculate_syntax_error_score(lines: List[str]) -> int:
    processed_lines = process_lines(lines)
    return reduce(lambda x, y: (0, 0, x[2] + y[2]), processed_lines)[2]


# PART 2
def evaluate_incomplete(validation_result):
    stack = validation_result[1]
    items = []
    while len(stack) > 0:
        items.append(stack.pop())
    # print(items)
    score = 0
    for symbol in items:
        score = score * 5 + incomplete_score[symbol]
    return score


def get_best_incomplete_score(lines: List[ValidationResult]) -> int:
    processed_lines = process_lines(lines)
    incomplete_lines = [line for line in processed_lines if line[0] == ValidationResult.INCOMPLETE]
    incomplete_valuations = sorted(list(map(evaluate_incomplete, incomplete_lines)))
    return incomplete_valuations[len(incomplete_valuations) // 2]


if __name__ == '__main__':
    with open('data/aoc2021-input-day10.txt', 'r') as f:
        sol_raw_instructions = [line.strip('\n') for line in f.readlines()]

    # PART 1
    print('PART 1:')
    print('>>>SOLUTION:', calculate_syntax_error_score(sol_raw_instructions))

    # PART 2
    print('PART 2:')
    print('>>>SOLUTION:', get_best_incomplete_score(sol_raw_instructions))
