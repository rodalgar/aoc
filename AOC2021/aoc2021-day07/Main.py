# Day 7: The Treachery of Whales
from collections import Counter
from functools import lru_cache
from typing import List, Callable


def parse_input(raw_data: str) -> List[int]:
    return list(map(int, raw_data.split(',')))


def calculate_fuel_constant(absolute_distance: int) -> int:
    """
    It's a silly function but allows re-using all the code by passing other more complex fuel calculation functions.
    First I thought of passing the two position values (crab's , and probing) but on more complex functions I will want
    to cache the call for a given distance no matter what the actual positions are (ie. distance 1 is achieved by 7 - 6,
    and 3 - 2, or even 4 - 5)

    :param absolute_distance: zero or positive distance to calculate
    :return: fuel consumption at a constant rate
    """
    return absolute_distance


@lru_cache(maxsize=None)
def calculate_fuel_accumulating(absolute_distance: int) -> int:
    """
    Calculates the fuel consumption at a constant linear incremental rate. See comments at calculate_fuel_constant.
    :param absolute_distance:
    :return:
    """
    return sum(range(absolute_distance + 1))


def get_minimum_v6(positions: List[int], fuel_calculator: Callable[[int], int]) -> int:
    """
    All crabs with the same horizontal position are the same to us, so we can just count how many of them are at a given
    position and then multiply costs from that position to the final position and multiply by the number of crabs.
    Once a minimum is calculated (first computation) every other posibility is tested against that value so if we detect
    that another position is not going to improve the result we stop that one and try another.
    This code can be improved, among other things by sorting crab positions every time we change the probing position.
    :param positions:
    :param fuel_calculator:
    :return:
    """
    crabs_per_position = Counter(positions)
    reduced_positions = crabs_per_position.keys()
    sorted_crab_positions = sorted(reduced_positions)
    min_fuel_global = None
    for pos_iter in range(sorted_crab_positions[-1] + 1):
        min_fuel = 0
        for position in sorted_crab_positions:
            min_fuel += fuel_calculator(abs(position - pos_iter)) * crabs_per_position[position]
            if min_fuel_global is not None and min_fuel >= min_fuel_global:
                break
        if min_fuel_global is None or min_fuel < min_fuel_global:
            min_fuel_global = min_fuel
    return min_fuel_global


if __name__ == '__main__':
    with open('data/aoc2021-input-day07.txt', 'r') as f:
        raw_crabs = f.readline()

    crabs = parse_input(raw_crabs)

    print('PART 1:')
    print('>>>SOLUTION: ', get_minimum_v6(crabs, calculate_fuel_constant))

    print('PART 2:')
    print('>>>SOLUTION: ', get_minimum_v6(crabs, calculate_fuel_accumulating))
