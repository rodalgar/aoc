# Day 10: Hoof It

def get_starting_positions(raw_data: [str]) -> [(int, int)]:
    return [(n_row, n_col)
            for n_row, line in enumerate(raw_data)
            for n_col, j in enumerate(line)
            if line[n_col] == '0']


def follow_trailhead_rec(row: int, col: int, actual_level: int, map_data: [str]) -> (int, {(int, int)}):
    # base case, we reach the peak!
    if actual_level == 9:
        return 1, {(row, col)}

    map_geometry = len(map_data), len(map_data[0])
    total_adjacent = 0
    peaks_reached = set()
    # for each adjacent
    for direction in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        new_row, new_col = row + direction[0], col + direction[1]
        # bounded adjacent?
        if not (0 <= new_row < map_geometry[0]) or not (0 <= new_col < map_geometry[1]):
            continue
        # impassable?
        adjacent_symbol = map_data[new_row][new_col]
        if adjacent_symbol == '.':
            continue
        # not too steep
        adjacent_level = int(adjacent_symbol)
        if not (adjacent_level - actual_level == 1):
            continue
        # adjacent is ok, let's see how it ends...
        sum_adjacent, peaks = follow_trailhead_rec(new_row, new_col, adjacent_level, map_data)
        total_adjacent += sum_adjacent
        for peak in peaks:
            peaks_reached.add(peak)

    return total_adjacent, peaks_reached


# PART 1
def calculate_trailhead_score(map_data: [str]) -> int:
    trails = [follow_trailhead_rec(starting_position[0], starting_position[1], 0, map_data)
              for starting_position
              in get_starting_positions(map_data)]
    return sum([len(peaks) for n_paths, peaks in trails])


# PART 2
def calculate_trailhead_rating(map_data: [str]) -> int:
    trails = [follow_trailhead_rec(starting_position[0], starting_position[1], 0, map_data)
              for starting_position
              in get_starting_positions(map_data)]
    return sum([n_paths for n_paths, peaks in trails])


if __name__ == '__main__':
    with open('data/aoc2024-input-day10.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    print('>>>>SOLUTION: ', calculate_trailhead_score(sol_raw_data))

    print('PART 2')
    print('>>>>SOLUTION: ', calculate_trailhead_rating(sol_raw_data))
