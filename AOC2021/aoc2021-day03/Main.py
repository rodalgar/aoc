# Day 3: Binary Diagnostic
from typing import List, Tuple


# PART 1
def get_common_bits_at(diagnostic: List[str], position: int) -> Tuple[str, str]:
    ones_at = sum(map(int, [line[position] for line in diagnostic]))
    most_common_bit = 1 if ones_at > len(diagnostic) / 2 else 0
    least_common_bit = 1 - most_common_bit
    return str(most_common_bit), str(least_common_bit)


def get_gamma_epsilon_rates(diagnostic: List[str]) -> Tuple[int, int]:
    length_items = len(diagnostic[0])
    gamma_rate = 0
    epsilon_rate = 0
    for i in range(length_items):
        most, least = get_common_bits_at(diagnostic, i)
        gamma_rate += 2 ** (length_items - i - 1) * int(most)
        epsilon_rate += 2 ** (length_items - i - 1) * int(least)
    return gamma_rate, epsilon_rate


# PART 2
def get_life_support_rates(diagnostics: List[str]) -> Tuple[int, int]:
    length_items = len(diagnostics[0])
    oxygen_data = diagnostics[:]
    co2_data = diagnostics[:]
    for i in range(length_items):
        # oxygen
        ones_at = sum(map(int, [line[i] for line in oxygen_data]))
        zeros_at = len(oxygen_data) - ones_at
        filter_value = '1' if ones_at >= zeros_at else '0'
        oxygen_data = [line for line in oxygen_data if line[i] == filter_value]
        if len(oxygen_data) == 1:
            break
    for i in range(length_items):
        ones_at = sum(map(int, [line[i] for line in co2_data]))
        zeros_at = len(co2_data) - ones_at
        filter_value = '0' if zeros_at <= ones_at else '1'
        co2_data = [line for line in co2_data if line[i] == filter_value]
        if len(co2_data) == 1:
            break

    oxygen_rate = oxygen_data[0]
    co2_rate = co2_data[0]

    return int(oxygen_rate, 2), int(co2_rate, 2)


if __name__ == '__main__':
    with(open('data/aoc2021-input-day03.txt', 'r')) as f:
        sol_raw = [line.strip('\n') for line in f.readlines()]

    # PART 1
    sol_gamma_rate, sol_epsilon_rate = get_gamma_epsilon_rates(sol_raw)
    print('PART 1')
    print('>>>SOLUTION: ', sol_gamma_rate * sol_epsilon_rate)

    # PART 2
    sol_oxygen, sol_co2 = get_life_support_rates(sol_raw)
    print('PART 2')
    print('>>>SOLUTION: ', sol_oxygen * sol_co2)
