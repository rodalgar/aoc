# Day 6: Lanternfish
from typing import List


def parse_input(raw_input: str) -> List[int]:
    # All fish with the same timer are equal to their fellow same-timer fish so
    # we group each fish per its timer. So we can advance every one of them at once.
    parsed_input = 10 * [0]
    # fish will be stored at "timer + 1" position, so timer 6 will be position 7
    # this is on purpose so we have the fist position store timer -1 which are the
    # fish that were at timer 0 at the beginning of the day so we don't have to do
    # any special treatment to timers 6 and 8 during computation.
    for fish in map(int, raw_input.split(',')):
        parsed_input[fish + 1] += 1
    return parsed_input


def process_day(fish_data: List[int]) -> None:
    # let's count a day to each fish
    for position in range(1, 10):
        fish_data[position - 1] = fish_data[position]
    # fish at -1 (0) were at 0 (1) this turn, so:
    # 1. renew. fish at -1 (0) become 6 (7) again
    fish_data[7] += fish_data[0]
    # 2. each fish at -1 (0) create a new fish at 8 (9)
    fish_data[9] = fish_data[0]
    # 3. clean after the party
    fish_data[0] = 0


def process_days(fish_data_in: List[int], n_days: int) -> int:
    fish_data = fish_data_in[:]
    for i in range(n_days):
        process_day(fish_data)
    return sum(fish_data)


if __name__ == '__main__':
    with open('data/aoc2021-input-day06.txt', 'r') as f:
        sol_fish_raw_data = f.readline().strip('\n')

    print('PART 1')
    sol_fish_data = parse_input(sol_fish_raw_data)
    sol_total_fish = process_days(sol_fish_data, 80)
    print('>>>SOLUTION: ', sol_total_fish)

    print('PART 2')
    sol_total_fish = process_days(sol_fish_data, 256)
    print('>>>SOLUTION: ', sol_total_fish)
