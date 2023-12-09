# Day 9: Mirage Maintenance

def parse_input(raw_data: list[str]) -> list[list[int]]:
    return [list(map(int, line.split(' '))) for line in raw_data]


def unified_extrapolate_sequence(sequence: list[int]) -> tuple[int, int]:
    actual_seq = sequence
    first_values = [actual_seq[0]]
    last_values = [actual_seq[-1]]
    while any((x for x in actual_seq if x != 0)):
        new_seq = [actual_seq[i] - actual_seq[i-1] for i in range(1, len(actual_seq))]
        first_values.append(new_seq[0])
        last_values.append(new_seq[-1])
        actual_seq = new_seq

    # first extrapolated value
    first_extrapolation = first_values[-1]
    for i in range(len(first_values) - 2, -1, -1):
        first_extrapolation = first_values[i] - first_extrapolation

    # last extrapolated value
    last_extrapolation = sum(last_values)

    return first_extrapolation, last_extrapolation


def unified_extrapolate(sequences: list[list[int]]) -> tuple[int, int]:
    data = [unified_extrapolate_sequence(seq) for seq in sequences]

    first_total = sum(x[0] for x in data)
    last_total = sum(x[1] for x in data)

    return first_total, last_total


if __name__ == '__main__':
    with open('data/aoc2023-input-day09.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_data = parse_input(sol_raw_data)

    part2_extrapolation, part1_extrapolation = unified_extrapolate(sol_data)

    print('PART 1')
    print('>>>>SOLUTION: ', part1_extrapolation)

    print('PART 2')
    print('>>>>SOLUTION: ', part2_extrapolation)
