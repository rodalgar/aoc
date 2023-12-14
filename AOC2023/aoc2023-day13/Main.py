# Day 13: Point of Incidence
from typing import Optional

VERTICAL_MIRROR = 0
HORIZONTAL_MIRROR = 1


def parse_input(raw_data: list[str]) -> list[tuple[list[str], list[str]]]:
    patterns = []
    pattern = []
    for line in raw_data:
        if len(line) == 0:
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    if len(pattern) > 0:
        patterns.append(pattern)

    transposed_patterns = []
    for pattern in patterns:
        transposed_pattern = []

        for i in range(len(pattern[0])):
            transposed_line = [line[i] for line in pattern]
            transposed_pattern.append(''.join(transposed_line))
        transposed_patterns.append(transposed_pattern)

    return [(p, pt) for p, pt in zip(patterns, transposed_patterns)]


def locate_mirror_in_pattern(pattern: list[str]) -> Optional[tuple[int, int]]:
    i_mirror = None
    for i in range(len(pattern) - 1):
        if pattern[i] == pattern[i + 1]:
            left = i
            right = i + 1
            are_equal = True
            while are_equal and left >= 0 and right < len(pattern):
                are_equal = pattern[left] == pattern[right]
                left -= 1
                right += 1
            if are_equal:
                # problem is one-based counting
                i_mirror = (i + 1, i + 2)
                break
    return i_mirror


def locate_mirrors(data: tuple[list[str], list[str]]) -> Optional[tuple[int, tuple[int, int], list[str], list[str]]]:
    pattern, transposed_pattern = data

    pattern_mirror = locate_mirror_in_pattern(pattern)

    transposed_pattern_mirror = locate_mirror_in_pattern(transposed_pattern)

    if pattern_mirror is not None:
        return HORIZONTAL_MIRROR, pattern_mirror, pattern, transposed_pattern
    if transposed_pattern_mirror is not None:
        return VERTICAL_MIRROR, transposed_pattern_mirror, pattern, transposed_pattern
    return None


def part1(data: list[tuple[list[str], list[str]]]) -> int:
    mirrors = [locate_mirrors(patterns) for patterns in data]

    total = 0
    for mirror in mirrors:
        if mirror[0] == VERTICAL_MIRROR:
            total += mirror[1][0]
        else:
            total += 100 * mirror[1][0]
    return total


def locate_smudge_in_pattern(pattern: list[str], mirror_line: int = None) -> tuple[int, int]:
    i_mirror = None
    for i in range(len(pattern) - 1):
        # ignore possible smudges on the same position as the current mirror
        if mirror_line is not None and (mirror_line - 1) == i:
            continue

        left = i
        right = i + 1
        smudges = 0
        are_equal = True
        while are_equal and left >= 0 and right < len(pattern):
            inner_diffs = [ix
                           for ix, (position_l, position_r) in enumerate(zip(pattern[left], pattern[right]))
                           if position_l != position_r]
            if len(inner_diffs) > 1:
                are_equal = False
                break
            smudges += len(inner_diffs)
            if smudges > 1:
                are_equal = False
                break
            left -= 1
            right += 1
        if are_equal:
            # one-based counting
            i_mirror = (i + 1, i + 2)
            break
    return i_mirror


def part2(data: list[tuple[list[str], list[str]]]) -> int:
    total = 0
    for ix, patterns in enumerate(data):

        mirror = locate_mirror_in_pattern(patterns[0])
        smudge = locate_smudge_in_pattern(patterns[0], mirror[0] if mirror is not None else None)
        smudge_type = HORIZONTAL_MIRROR
        if smudge is None:
            mirror = locate_mirror_in_pattern(patterns[1])
            smudge = locate_smudge_in_pattern(patterns[1], mirror[0] if mirror is not None else None)
            smudge_type = VERTICAL_MIRROR

        if smudge_type == VERTICAL_MIRROR:
            total += smudge[0]
        else:
            total += 100 * smudge[0]
    return total


if __name__ == '__main__':
    with open('data/aoc2023-input-day13.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_data = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', part1(sol_data))

    print('PART 2')
    print('>>>>SOLUTION: ', part2(sol_data))
