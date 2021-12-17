# Day 15: Chiton
import itertools
import re
from typing import List


def parse_input(raw_input: List[str]) -> List[List[int]]:
    return list(map(lambda x: list(map(int, x)), map(re.findall, itertools.repeat(r"\d"), raw_input)))


def key(row_pos: int, col_pos: int) -> str:
    return f'{row_pos}-{col_pos}'


# PART 1
def print_path(the_path, max_row, max_col):
    for row in range(max_row + 1):
        the_row = []
        for col in range(max_col + 1):
            if key(row, col) in the_path:
                the_row.append(the_path[key(row, col)][0])
            else:
                the_row.append(-1)
        print('\t'.join(map(str, the_row)))


def find_path(the_map: List[List[int]]):
    def distance(row0: int, col0: int, row1: int, col1: int) -> int:
        return abs(row1 - row0) + abs(col1 - col0)

    max_row = len(the_map) - 1
    max_col = len(the_map[0]) - 1
    row_goal = max_row
    col_goal = max_col
    starting_row = 0
    starting_col = 0

    # initialize with top-left element at 0,0 with cost and no parent
    visited = {key(0, 0): (0, None)}
    to_visit = [(0, 0, 0, distance(starting_row, starting_col, row_goal, col_goal), None)]

    while len(to_visit) > 0:
        to_visit = sorted(to_visit, key=lambda x: x[2] + x[3])

        step = to_visit[0]
        to_visit = to_visit[1:]

        row, col, cost, estimated_cost, parent = step

        if row == row_goal and col == col_goal:
            # we did it!
            print('ok', cost, visited[key(row, col)], len(to_visit), len(visited))
            break

        # each iteration is an adjacent
        for delta in [[-1, 0], [1, 0], [0, 1], [0, -1]]:
            new_row = row + delta[0]
            new_col = col + delta[1]

            # not visiting parent again :D
            # if parent is not None and new_row == parent[0] and new_col == parent[1]:
            #     continue

            # valid adjacent?
            if new_row < 0 or new_row > max_row or new_col < 0 or new_col > max_col:
                continue

            cost_to_visit = the_map[new_row][new_col] + cost
            my_remaining_estimated_cost = distance(new_row, new_col, row_goal, col_goal)

            if key(new_row, new_col) in visited:
                # tile already visited
                already_visited = visited[key(new_row, new_col)]
                if already_visited[0] > cost_to_visit + my_remaining_estimated_cost:
                    visited[key(new_row, new_col)] = (cost_to_visit, (row, col))
                    to_visit.append((new_row, new_col, cost_to_visit, my_remaining_estimated_cost, (row, col)))
            else:
                # first time visiting tile
                visited[key(new_row, new_col)] = (cost_to_visit, (row, col))
                if key(row_goal, col_goal) in visited:
                    visited_goal = visited[key(row_goal, col_goal)]
                    if visited_goal[0] >= cost_to_visit:
                        to_visit.append((new_row, new_col, cost_to_visit, my_remaining_estimated_cost, (row, col)))
                else:
                    to_visit.append((new_row, new_col, cost_to_visit, my_remaining_estimated_cost, (row, col)))

    return visited[key(row_goal, col_goal)][0]


# PART 2
def expand_map(original_map, n_blocks=2):
    def new_value(x, increment):
        incremented_value = x + increment
        if incremented_value > 9:
            incremented_value -= 9
        return incremented_value

    # First we expand the columns
    new_map = original_map.copy()
    for i in range(1, n_blocks):
        for row in range(len(original_map)):
            new_block = [new_value(x, i) for x in original_map[row]]
            new_map[row] = new_map[row] + new_block

    # Know we expand the rows
    for i in range(1, n_blocks):
        for row in range(len(original_map)):
            new_block = [new_value(x, i) for x in new_map[row]]
            new_map.append(new_block)

    return new_map


if __name__ == '__main__':
    with open('data/aoc2021-input-day15.txt', 'r') as f:
        sol_raw_instructions = [line.strip('\n') for line in f.readlines()]

    sol_map = parse_input(sol_raw_instructions)
    # PART 1
    print('PART 1')
    print('>>>SOLUTION:', find_path(sol_map))

    # PART 2
    expanded_sol_map = expand_map(sol_map, n_blocks=5)
    print('PART 2')
    print('>>>SOLUTION:', find_path(expanded_sol_map))
