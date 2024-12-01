# Day 10: Pipe Maze
from Tile import Tile
from TileTemplate import TileTemplate

map_tiles = [
    TileTemplate('-', (3, 1), True),
    TileTemplate('|', (0, 2), True),
    TileTemplate('F', (1, 2), True),
    TileTemplate('L', (0, 1), True),
    TileTemplate('J', (0, 3), True),
    TileTemplate('7', (3, 2), True),
    TileTemplate('.', None, False),
    TileTemplate('S', (-1, -1), True)
]

directions = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1)
}


def parse_input(raw_data: [str]) -> tuple[tuple[int, int], list[list[Tile]]]:
    map_conversions = {tile_template.glyph: tile_template for tile_template in map_tiles}
    map_data = []
    init_position = None
    for ix, line in enumerate(raw_data):
        map_row = []
        starting_index = line.find('S')
        if starting_index != -1:
            init_position = (ix, starting_index)
        for pos in line:
            tile = Tile()
            if pos in map_conversions:
                tile.tile_template = map_conversions[pos]
            map_row.append(tile)
        map_data.append(map_row)
    return init_position, map_data


def print_map(map_to_print):
    for line in map_to_print:
        for tile in line:
            print(tile, end='\t\t')
        print()


# PART 1
def navigate_both(starting_position, map_data, verbose=False):
    # find heads and direction
    if verbose:
        print('starting_position', starting_position)
    starting_map_tile = map_data[starting_position[0]][starting_position[1]]
    starting_map_tile.is_path = True

    head_paths = []
    starting_path_direction = []
    for ix in [0, 1, 2, 3]:
        delta_direction = directions[ix]
        starting_adjacent = (starting_position[0] + delta_direction[0], starting_position[1] + delta_direction[1])

        if starting_adjacent[0] < 0 or starting_adjacent[0] > len(map_data):
            continue
        if starting_adjacent[1] < 0 or starting_adjacent[1] > len(map_data[0]):
            continue
        adjacent_map_tile = map_data[starting_adjacent[0]][starting_adjacent[1]]

        # adjacent is pipe?
        if not adjacent_map_tile.tile_template.is_pipe:
            continue

        # adjacent is connected with starting_position?
        if adjacent_map_tile.tile_template.direction is not None and (
                ix + 2) % 4 in adjacent_map_tile.tile_template.direction:
            starting_path_direction.append(ix)
            head_paths.append((starting_position, ix))
    starting_path_direction.reverse()
    starting_map_tile.path_direction = tuple(starting_path_direction)
    assert len(head_paths) == 2, \
        f'There should be two pipes connected to {starting_position} but there are {len(head_paths)}'

    if verbose:
        print(head_paths)
        print_map(map_data)
        print('---')

    # traverse both heads
    step = 0
    while True:
        forward = True
        if verbose:
            print('step: ', step)
        new_head_paths = []
        for head in head_paths:
            position, ix_direction = head
            delta_direction = directions[ix_direction]
            new_position = (position[0] + delta_direction[0], position[1] + delta_direction[1])
            map_position = map_data[new_position[0]][new_position[1]]

            if map_position.tile_template.direction == (-1, -1):
                continue
            opposite_direction = (ix_direction + 2) % 4
            new_ix_direction = map_position.tile_template.direction[0] \
                if map_position.tile_template.direction[1] == opposite_direction \
                else map_position.tile_template.direction[1]
            new_head_paths.append((new_position, new_ix_direction))

            map_position.is_path = True
            map_position.path_direction = (opposite_direction, new_ix_direction) \
                if forward \
                else (new_ix_direction, opposite_direction)

            forward = not forward
        step += 1
        if verbose:
            print(new_head_paths)
        if len(new_head_paths) != 2:
            break

        if verbose:
            print(f'head_paths[0]', head_paths[0], 'new_head_paths', new_head_paths)
            print(f'head_paths[1]', head_paths[1], 'new_head_paths', new_head_paths)
            print('cmp', new_head_paths[0][0], new_head_paths[1][0])

        if new_head_paths[0][0] == new_head_paths[1][0]:
            if verbose:
                print_map(map_data)
            break

        if (head_paths[0][0] == new_head_paths[1][0]) or (head_paths[1][0] in new_head_paths[0][0]):
            if verbose:
                print_map(map_data)
            break
        head_paths = new_head_paths

        if verbose:
            print_map(map_data)
    return step


# PART 2
def flood_map_from(starting_position, navigated_map):
    to_visit = [starting_position]

    while len(to_visit) > 0:
        next_to_visit = to_visit[:1][0]
        to_visit = to_visit[1:]

        next_to_visit_tile = navigated_map[next_to_visit[0]][next_to_visit[1]]
        if next_to_visit_tile.enclosing_type is not None:
            continue

        next_to_visit_tile.enclosing_type = Tile.INNER_ENCLOSING

        for ix in [0, 1, 2, 3]:
            delta_direction = directions[ix]
            adjacent_pos = (next_to_visit[0] + delta_direction[0], next_to_visit[1] + delta_direction[1])

            if adjacent_pos[0] < 0 or adjacent_pos[0] >= len(navigated_map):
                continue
            if adjacent_pos[1] < 0 or adjacent_pos[1] >= len(navigated_map[0]):
                continue
            adjacent_map_tile = navigated_map[adjacent_pos[0]][adjacent_pos[1]]

            if adjacent_map_tile.enclosing_type is not None:
                continue
            if adjacent_map_tile.is_path:
                continue

            if adjacent_pos not in to_visit:
                to_visit.append(adjacent_pos)


def get_enclosed_tiles(starting_position: tuple[int, int], navigated_map: list[list[Tile]], verbose: bool = False):
    if verbose:
        print_map(navigated_map)
    # get outer way
    LEFT_WAY = 0
    RIGHT_WAY = 1
    # testing order left to right, right to left, top to bottom, bottom to top
    outer_way = None
    for line in navigated_map:
        for tile in line:
            # must be in the path
            if not tile.is_path:
                continue
            if tile.path_direction in [(2, 0), (2, 1), (1, 0)]:
                outer_way = LEFT_WAY
                break
            if tile.path_direction in [(0, 2), (1, 2), (0, 1)]:
                outer_way = RIGHT_WAY
                break
            # can't be parallel in this direction, & any other combination are not possible
            if tile.path_direction in [(1, 3), (3, 1)]:
                break
        if outer_way is not None:
            break
    if outer_way is None:
        print('Unable to compute which way goes the path')

    if verbose:
        print('outer_way:', outer_way)

    starting_map_tile = navigated_map[starting_position[0]][starting_position[1]]
    head_tile = starting_map_tile
    head_position = starting_position
    while True:
        delta_directions = []
        if head_tile.path_direction == (2, 0):
            if outer_way == RIGHT_WAY:
                # trying flood to the left
                delta_directions.append((0, -1))
            else:
                # trying flood to the right
                delta_directions.append((0, 1))
        elif head_tile.path_direction == (0, 2):
            if outer_way == RIGHT_WAY:
                # trying flood to the right
                delta_directions.append((0, 1))
            else:
                # trying flood to the left
                delta_directions.append((0, -1))
        elif head_tile.path_direction == (3, 1):
            if outer_way == RIGHT_WAY:
                # trying flood upwards
                delta_directions.append((-1, 0))
            else:
                # trying flood downwards
                delta_directions.append((1, 0))
        elif head_tile.path_direction == (1, 3):
            if outer_way == RIGHT_WAY:
                # trying flood downwards
                delta_directions.append((1, 0))
            else:
                # trying flood upwards
                delta_directions.append((-1, 0))
        elif head_tile.path_direction == (3, 0):
            if outer_way == LEFT_WAY:
                delta_directions.append((0, 1))
                delta_directions.append((1, 0))
        elif head_tile.path_direction == (0, 3):
            if outer_way == RIGHT_WAY:
                delta_directions.append((0, 1))
                delta_directions.append((1, 0))
        elif head_tile.path_direction == (0, 1):
            if outer_way == LEFT_WAY:
                delta_directions.append((0, -1))
                delta_directions.append((1, 0))
        elif head_tile.path_direction == (1, 0):
            if outer_way == RIGHT_WAY:
                delta_directions.append((0, -1))
                delta_directions.append((1, 0))
        elif head_tile.path_direction == (1, 2):
            if outer_way == LEFT_WAY:
                delta_directions.append((0, -1))
                delta_directions.append((-1, 0))
        elif head_tile.path_direction == (2, 1):
            if outer_way == RIGHT_WAY:
                delta_directions.append((0, -1))
                delta_directions.append((-1, 0))
        elif head_tile.path_direction == (2, 3):
            if outer_way == LEFT_WAY:
                delta_directions.append((0, 1))
                delta_directions.append((-1, 0))
        elif head_tile.path_direction == (3, 2):
            if outer_way == RIGHT_WAY:
                delta_directions.append((0, 1))
                delta_directions.append((-1, 0))

        for delta_direction in delta_directions:
            position_adjacent = (head_position[0] + delta_direction[0], head_position[1] + delta_direction[1])
            if (0 <= position_adjacent[0] < len(navigated_map)) and (0 <= position_adjacent[1] < len(navigated_map[0])):
                position_map_tile = navigated_map[position_adjacent[0]][position_adjacent[1]]
                if not position_map_tile.is_path and position_map_tile.enclosing_type is None:
                    # flood at exact coordinates
                    flood_map_from(position_adjacent, navigated_map)

        # calculating next step of the path
        head_direction = head_tile.path_direction[1]
        head_delta_direction = directions[head_direction]
        next_head_position = (head_position[0] + head_delta_direction[0], head_position[1] + head_delta_direction[1])

        head_position = next_head_position
        head_tile = navigated_map[head_position[0]][head_position[1]]

        # computation ends if next step is starting position
        if head_tile.tile_template.glyph == 'S':
            break

    inner_tiles = [tile for row in navigated_map for tile in row if
                   tile.enclosing_type == Tile.INNER_ENCLOSING]

    if verbose:
        print('*+*+*+*+*')
        print_map(navigated_map)
        print(inner_tiles)
        print('*+*+*+*+*')
    return len(inner_tiles)


if __name__ == '__main__':
    with open('data/aoc2023-input-day10.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_init, sol_map = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', navigate_both(sol_init, sol_map))

    print('PART 2')
    print('>>>>SOLUTION: ', get_enclosed_tiles(sol_init, sol_map))
