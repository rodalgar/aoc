# Day 6: Guard Gallivant


directions = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1)
}

map_directions = {
    '^': 0,
    '>': 1,
    'v': 2,
    '<': 3
}


def parse_input(raw_data: [str]) -> ((int, int), int, [str]):
    starting_position = None
    starting_direction = None

    map_data = []
    for n_row, line in enumerate(raw_data):
        new_line = line
        if starting_position is None:
            for m_dir in map_directions.keys():
                if m_dir in line:
                    n_col = line.index(m_dir)
                    starting_position = (n_row, n_col)
                    starting_direction = map_directions[raw_data[n_row][n_col]]
                    new_line = line[:n_col] + 'O' + line[n_col + 1:]
                    break

        map_data.append(list(new_line))
    return starting_position, starting_direction, map_data


def traverse_map(starting_position, starting_direction, map_data, verbose=False):
    visited_tiles = {(starting_position, starting_direction)}
    path = [(starting_position, None)]
    max_row = len(map_data)
    max_col = len(map_data[0])
    position = starting_position
    ix_dir = starting_direction
    if verbose:
        print(f'starting position {starting_position} starting dir {starting_direction} '
              f'map bounds: max_row {max_row} max_col {max_col}')
    while True:
        direction = directions[ix_dir]
        new_position = position[0] + direction[0], position[1] + direction[1]

        if verbose:
            print(f'new pos is {new_position} direction {direction}')
        # checking bounds
        if not 0 <= new_position[0] < len(map_data):
            break
        if not 0 <= new_position[1] < len(map_data[0]):
            break

        # checking collision
        if map_data[new_position[0]][new_position[1]] == '#':
            # bump! don't walk only turn to the right
            ix_dir = (ix_dir + 1) % 4
            continue

        if (new_position, ix_dir) in visited_tiles:
            # cycle detected, breaking loop
            return path, True

        visited_tiles.add((new_position, ix_dir))
        path.append((new_position, ix_dir))
        position = new_position

    return path, False


def part1(starting_position, starting_direction, map_data):
    path, _ = traverse_map(starting_position, starting_direction, map_data)
    unique_steps = {step_position for step_position, step_dir in path}
    return len(unique_steps)


def part2(starting_position, starting_direction, map_data):
    original_path, _ = traverse_map(starting_position, starting_direction, map_data)
    new_object_placed = set()
    detected_cycles = 0
    for step_pos, step_dir in original_path[1:]:
        step_row, step_col = step_pos
        if (step_row, step_col) in new_object_placed:
            continue
        new_object_placed.add((step_row, step_col))
        map_data[step_row][step_col] = '#'
        modified_path, exit_by_cycle = traverse_map(starting_position, starting_direction, map_data)
        map_data[step_row][step_col] = '.'

        if exit_by_cycle:
            detected_cycles += 1
    return detected_cycles


if __name__ == '__main__':
    with open('data/aoc2024-input-day06.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_ini_pos, sol_dir, sol_map = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', part1(sol_ini_pos, sol_dir, sol_map))

    print('PART 2')
    print('>>>>SOLUTION: ', part2(sol_ini_pos, sol_dir, sol_map))
