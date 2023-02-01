# Day 13: Distress Signal
from functools import cmp_to_key

RIGHT_ORDER = -1
NOT_RIGHT_ORDER = 1
UNDETERMINED_ORDER = 0


def parse_input(raw):
    return [eval(line) for line in raw if len(line) > 0]


def compare(left_side, right_side):
    if isinstance(left_side, list) and isinstance(right_side, list):
        i = 0
        while i < len(left_side) and i < len(right_side):
            r = compare(left_side[i], right_side[i])
            if r != UNDETERMINED_ORDER:
                return r
            i += 1
        if i == len(left_side) and i == len(right_side):
            return UNDETERMINED_ORDER
        if i == len(left_side):
            return RIGHT_ORDER
        if i == len(right_side):
            return NOT_RIGHT_ORDER

    elif isinstance(left_side, int) and isinstance(right_side, int):
        return RIGHT_ORDER \
            if left_side < right_side else NOT_RIGHT_ORDER \
            if right_side < left_side else UNDETERMINED_ORDER

    else:
        if isinstance(left_side, int):
            left_side = [left_side]
        if isinstance(right_side, int):
            right_side = [right_side]
        return compare(left_side, right_side)


# PART 1
def part1(pair_list):
    right_pairs = []
    for x in range(0, len(pair_list), 2):
        r = compare(pair_list[x], pair_list[x + 1])
        if r == RIGHT_ORDER:
            right_pairs.append((x // 2) + 1)

    return sum(right_pairs)


# PART 2
def part2(pairs, verbose=False):
    DIVIDER_1 = [[2]]
    DIVIDER_2 = [[6]]
    pairs.append(DIVIDER_1)
    pairs.append(DIVIDER_2)

    k = cmp_to_key(compare)
    pairs.sort(key=k)
    if verbose:
        for l in pairs:
            print(l)

    ix1 = pairs.index(DIVIDER_1) + 1
    ix2 = pairs.index(DIVIDER_2) + 1
    return ix1, ix2, ix1 * ix2


if __name__ == '__main__':
    with open('data/aoc2022-input-day13.txt', 'r') as f:
        raw_data = [line.strip('\n') for line in f.readlines()]

    data = parse_input(raw_data)
    print('PART 1')
    print('>>>SOLUTION: ', part1(data))

    print('PART 2')
    _, _, sol = part2(data)
    print('>>>SOLUTION: ', sol)
