# Day 1: Sonar Sweep
from typing import List
import itertools


# PART 1
def depth_measurement_increments(depths: List[int]) -> int:
    """
    Given a list of sequential depths, obtains how many pressure increments.

    :param depths: List of integers representing depths
    :return: How many times an increment in pressure occurs.
    """
    return sum([1 for x, y in zip(depths[1:], depths[:len(depths)-1]) if x > y])


# PART 2
def rolling_sum(depths: List[int], window_size: int) -> List[int]:
    """
    Given a list of sequential depths and a window size n, obtains a new list in which every item is the sum of the
    elements in a rolling window of size n.

    :param depths: List of integers representing depths
    :param window_size: window size to accumulate readings.
    :return: New list with "smoothed" depth readings.
    """
    return [sum(itertools.islice(depths, i, i+window_size))
            for i in range(0, len(depths) - window_size + 1)]


if __name__ == '__main__':
    with open('data/aoc2021-input-day01.txt', 'r') as f:
        sol_depths = list(map(int, [line.strip('\n') for line in f.readlines()]))

    print('PART 1')
    print('>>>SOLUTION: ', depth_measurement_increments(sol_depths))

    print('PART 2')
    print('>>>SOLUTION', depth_measurement_increments(rolling_sum(sol_depths, 3)))
