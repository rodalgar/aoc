# Day 8: Haunted Wasteland
import math
from functools import reduce
from typing import Callable


def parse_input(raw_data: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    directions = raw_data[0]

    navigation = {}
    for line in raw_data[2:]:
        parts = line.split('=')
        origin = parts[0].strip()
        targets = parts[1].strip(' ()').replace(',', '').split(' ')
        navigation[origin] = (targets[0], targets[1])

    return directions, navigation


def ending_condition_part1(option: str) -> bool:
    return option == 'ZZZ'


def navigate_one_path(directions: str, navigation: dict[str, tuple[str, str]],
                      starting_node: str, is_ending_node_fun: Callable[[str], bool]) -> int:
    option = starting_node
    step = 0
    limit = len(directions)

    while not is_ending_node_fun(option):
        node = navigation[option]
        way = directions[step % limit]
        if way == 'L':
            option = node[0]
        else:
            option = node[1]
        step += 1

    return step


# PART 2
def ending_condition_part2(option: str) -> bool:
    return option[-1] == 'Z'


def navigate_paths(directions: str, navigation: dict[str, tuple[str, str]]) -> int:
    starting_nodes = [k for k, v in navigation.items() if k[-1] == 'A']

    steps = [navigate_one_path(directions, navigation, starting_node, ending_condition_part2)
             for starting_node in starting_nodes]

    return int(reduce(math.lcm, steps))


if __name__ == '__main__':
    with open('data/aoc2023-input-day08.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_d, sol_n = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', navigate_one_path(sol_d, sol_n, 'AAA', ending_condition_part1))

    print('PART 2')
    print('>>>>SOLUTION: ', navigate_paths(sol_d, sol_n))
