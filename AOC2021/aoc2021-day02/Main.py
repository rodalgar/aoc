# Day 2: Dive!
from typing import Tuple, List
from functools import reduce


# PART 1
def parse_path(raw_path: List[str]) -> List[Tuple[Tuple[int, int], int]]:
    def parse_step(step: str) -> Tuple[str, int]:
        direction, magnitude = step.split(' ')
        if direction == 'forward':
            sub_dir = (1, 0)
        elif direction == 'up':
            sub_dir = (0, -1)
        elif direction == 'down':
            sub_dir = (0, 1)
        else:
            sub_dir = (0, 0)
            print(f'Unknown direction {direction}!')

        return sub_dir, int(magnitude)

    return list(map(parse_step, raw_path))


def resolve_path_from(instructions: List[Tuple[Tuple[int, int], int]], origin: Tuple[int, int]) -> Tuple[int, int]:
    def calculate_step(step: Tuple[Tuple[int, int], int]) -> Tuple[int, int]:
        direction, magnitude = step
        return direction[0] * magnitude, direction[1] * magnitude

    def apply_step(step: Tuple[int, int], position: Tuple[int, int]) -> Tuple[int, int]:
        return step[0] + position[0], step[1] + position[1]

    final_position = reduce(apply_step, map(calculate_step, instructions))

    return apply_step(final_position, origin)


# PART 2
def resolve_path_from_v2(instructions: List[Tuple[Tuple[int, int], int]], origin: Tuple[int, int]) -> Tuple[int, int]:
    def calculate_step(instruction: Tuple[Tuple[int, int], int]) -> Tuple[int, int, int]:
        direction, magnitude = instruction
        return direction[0] * magnitude, direction[0] * magnitude, direction[1] * magnitude

    position = origin
    for step in map(calculate_step, instructions):
        position = step[0] + position[0], step[1] * position[2] + position[1], step[2] + position[2]

    return position[0], position[1]


if __name__ == '__main__':
    with open('data/aoc2021-input-day02.txt', 'r') as f:
        sol_raw_instructions = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    sol_path = parse_path(sol_raw_instructions)
    sol_origin = (0, 0)
    sol_final_pos = resolve_path_from(sol_path, sol_origin)
    print('>>>SOLUTION:', sol_final_pos[0] * sol_final_pos[1])

    print('PART 2')
    sol_origin = (0, 0, 0)
    sol_final_pos = resolve_path_from_v2(sol_path, sol_origin)
    print('>>>SOLUTION:', sol_final_pos[0] * sol_final_pos[1])
