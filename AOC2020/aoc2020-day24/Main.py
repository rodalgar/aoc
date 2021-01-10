# Day 24: Lobby Layout

DIR_E = 'e'
DIR_W = 'w'
DIR_NE = 'ne'
DIR_NW = 'nw'
DIR_SE = 'se'
DIR_SW = 'sw'

TILE_WHITE = 1
TILE_BLACK = 0


def parse_raw_path(raw_path):
    """
    Parses a string representing the path from the reference tile to another into a list of steps

    :param raw_path: String representing a path.
    :return: List of steps.
    """
    parsed_path = []
    ix = 0
    while True:
        if raw_path[ix] == 'e':
            parsed_path.append(DIR_E)
        elif raw_path[ix] == 'w':
            parsed_path.append(DIR_W)
        elif raw_path[ix] in {'n', 's'} and len(raw_path) == ix + 1:
            raise IndexError(f'Unexpected end of path at {ix}. Started {raw_path[ix]} but "e" or "w" is missing!')
        elif raw_path[ix] == 'n' and raw_path[ix + 1] == 'e':
            parsed_path.append(DIR_NE)
            ix += 1
        elif raw_path[ix] == 'n' and raw_path[ix + 1] == 'w':
            parsed_path.append(DIR_NW)
            ix += 1
        elif raw_path[ix] == 's' and raw_path[ix + 1] == 'e':
            parsed_path.append(DIR_SE)
            ix += 1
        elif raw_path[ix] == 's' and raw_path[ix + 1] == 'w':
            parsed_path.append(DIR_SW)
            ix += 1
        else:
            raise ValueError(f'Unexpected symbol at {ix}: {raw_path[ix]}')

        ix += 1
        if ix == len(raw_path):
            break

    return parsed_path


def parse_raw_paths(raw_paths):
    """
    Parses a list of strings representing paths from the reference tile to others into a list of steps.

    :param raw_paths: List of strings representing paths.
    :return: List of parsed paths.
    """
    parsed_paths = []
    for raw_path in raw_paths:
        parsed_paths.append(parse_raw_path(raw_path))

    return parsed_paths


def calculate_tile_coordinates_hexagon(parsed_path):
    """
    Given a path, calculates which tile it leads to from reference tile at (0, 0).
    :param parsed_path: List of steps.
    :return: Tuple (x, y) being x and y coordinates of the tile at the end of the path.
    """
    tile_x, tile_y = 0, 0
    for step in parsed_path:
        is_left_leaning_row = tile_y % 2 == 0
        if step == DIR_W:
            tile_x -= 1
        elif step == DIR_E:
            tile_x += 1
        elif step == DIR_NW:
            tile_y -= 1
            if is_left_leaning_row:
                tile_x -= 1
        elif step == DIR_NE:
            tile_y -= 1
            if not is_left_leaning_row:
                tile_x += 1
        elif step == DIR_SW:
            tile_y += 1
            if is_left_leaning_row:
                tile_x -= 1
        elif step == DIR_SE:
            tile_y += 1
            if not is_left_leaning_row:
                tile_x += 1
    return tile_x, tile_y


def toggle_tile_color(actual_color):
    """
    Given a color it returns its opposite.

    :param actual_color: Color to toggle.
    :return: Toggled color.
    """
    if actual_color == TILE_WHITE:
        return TILE_BLACK
    else:
        return TILE_WHITE


def flip_tiles(instructions, calculate_coordinates_fun):
    """
    Sets the initial map based in a set of instructions (paths).

    :param instructions: List of parsed paths.
    :param calculate_coordinates_fun: Function used to resolve paths to tiles.
    :return: Dictionary representing the map, with keys as tuple of coordinates and values as colors.
    """
    the_map = {}

    for tile_path in instructions:
        tile_coordinates = calculate_coordinates_fun(tile_path)
        if tile_coordinates not in the_map:
            # By default, tile color is white so, if tile was not processed yet it is considered to be white.
            # We flip it into black.
            the_map[tile_coordinates] = TILE_BLACK
        else:
            # Tile was already processed, flipping value.
            last_value = the_map[tile_coordinates]
            the_map[tile_coordinates] = toggle_tile_color(last_value)

    return the_map


def count_black_tiles(flipped_map):
    """Counts how many tiles in a map are black."""
    return list(flipped_map.values()).count(TILE_BLACK)


def calculate_adjacent_tiles(tile_origin):
    """Given a tuple of coordinates, returns a list of tuple with the coordinates of the adjacent tiles in a hexagonal
    grid."""
    adjacent_tiles = []
    tile_x, tile_y = tile_origin
    # Adding w, e
    adjacent_tiles.append((tile_x + 1, tile_y))
    adjacent_tiles.append((tile_x - 1, tile_y))

    # row offset (representing an hex-grid with an squared-grid by offsetting every odd row, in this case)
    is_left_leaning_row = tile_y % 2 == 0

    east_modification = 0
    if not is_left_leaning_row:
        east_modification = 1
    west_modification = 0
    if is_left_leaning_row:
        west_modification = -1

    # nw
    adjacent_tiles.append((tile_x + west_modification, tile_y - 1))
    # ne
    adjacent_tiles.append((tile_x + east_modification, tile_y - 1))
    # sw
    adjacent_tiles.append((tile_x + west_modification, tile_y + 1))
    # se
    adjacent_tiles.append((tile_x + east_modification, tile_y + 1))

    return adjacent_tiles


def get_color_of_new_tile(the_map, tile):
    """Given a new tile in the map, calculate its initial color."""
    color_out = TILE_WHITE

    n_black_tiles = 0
    for adj in calculate_adjacent_tiles(tile):
        if adj in the_map and the_map[adj] == TILE_BLACK:
            n_black_tiles += 1

    # Untouched tile should be white but...
    if n_black_tiles == 2:
        color_out = TILE_BLACK

    return color_out


def pass_day(the_map, calculated_adjacent_tiles={}, verbose=False):
    """Passes one day, flipping tiles as per problem rules. It can use a pre-calculated list of adjacent tiles if
    passed."""
    new_map = {}

    for tile, color in the_map.items():
        if verbose:
            print(f'Processing tile {tile} of color {"WHITE" if color == TILE_WHITE else "BLACK"}')
        if tile not in calculated_adjacent_tiles:
            calculated_adjacent_tiles[tile] = calculate_adjacent_tiles(tile)
        n_adjacent_blacks = 0
        for adjacent in calculated_adjacent_tiles[tile]:
            if verbose:
                print(f'\t\t{adjacent}')
            # new value, untouched tiles, are white
            if adjacent not in the_map:
                new_map[adjacent] = get_color_of_new_tile(the_map, adjacent)
            else:
                if the_map[adjacent] == TILE_BLACK:
                    n_adjacent_blacks += 1

        new_map[tile] = color
        if color == TILE_WHITE:
            if verbose:
                print(f'\tTile is color TILE_WHITE, black adjacent tiles should be == 2 to flip. '
                      f'Black adjacent tiles: {n_adjacent_blacks}')
            if n_adjacent_blacks == 2:
                if verbose:
                    print(f'\t\tFLIP to TILE_BLACK')
                new_map[tile] = TILE_BLACK
        else:
            if verbose:
                print(
                    f'\tTile is color TILE_BLACK, black adjacent tiles should be 0 or > 2 to flip. '
                    f'Black adjacent tiles: {n_adjacent_blacks}')
            if n_adjacent_blacks == 0 or n_adjacent_blacks > 2:
                if verbose:
                    print(f'\t\tFLIP to TILE_WHITE')
                new_map[tile] = TILE_WHITE

    return new_map, calculated_adjacent_tiles


def pass_days(the_map, n_days, sample_days=[], verbose=False):
    """Passes n_days flipping color of tiles as per problem rules. It returns the final map and a list of counted
    black tiles at designated days in sample_days (if provided)"""
    adj = {}
    sampled_results = []

    for n_day in range(1, n_days + 1):
        the_map, adj = pass_day(the_map, adj, verbose)
        if n_day in sample_days:
            n_black_tiles = count_black_tiles(the_map)
            sampled_results.append((n_day, n_black_tiles))
            if verbose:
                print(f'Day {n_day}: {n_black_tiles}')

    return the_map, sampled_results


def test_parse_paths(raw_paths, expected, index):
    """Utility function to test parse_raw_paths."""
    test_parsed = parse_raw_paths(raw_paths)
    print(f'Testing parse_raw_paths ({index})',
          'RIGHT' if test_parsed == expected
          else f'WRONG!! Expected {expected} but was {test_parsed}')


if __name__ == '__main__':
    with open('data/aoc2020-input-day24.txt', 'r') as f:
        sol_raw_paths = [line.strip('\n') for line in f.readlines()]

    test_path_1 = ['esenee']
    test_path_2 = ['esew']
    test_path_3 = ['nwwswee']

    test_path_4 = [
        'sesenwnenenewseeswwswswwnenewsewsw',
        'neeenesenwnwwswnenewnwwsewnenwseswesw',
        'seswneswswsenwwnwse',
        'nwnwneseeswswnenewneswwnewseswneseene',
        'swweswneswnenwsewnwneneseenw',
        'eesenwseswswnenwswnwnwsewwnwsene',
        'sewnenenenesenwsewnenwwwse',
        'wenwwweseeeweswwwnwwe',
        'wsweesenenewnwwnwsenewsenwwsesesenwne',
        'neeswseenwwswnwswswnw',
        'nenwswwsewswnenenewsenwsenwnesesenew',
        'enewnwewneswsewnwswenweswnenwsenwsw',
        'sweneswneswneneenwnewenewwneswswnese',
        'swwesenesewenwneswnwwneseswwne',
        'enesenwswwswneneswsenwnewswseenwsese',
        'wnwnesenesenenwwnenwsewesewsesesew',
        'nenewswnwewswnenesenwnesewesw',
        'eneswnwswnwsenenwnwnwwseeswneewsenese',
        'neswnwewnwnwseenwseesewsenwsweewe',
        'wseweeenwnesenwwwswnew']

    print('PART 1')
    # TEST PART 1
    expected_parsed_path_1 = [[DIR_E, DIR_SE, DIR_NE, DIR_E]]
    test_parse_paths(test_path_1, expected_parsed_path_1, 1)

    expected_parsed_path_2 = [[DIR_E, DIR_SE, DIR_W]]
    test_parse_paths(test_path_2, expected_parsed_path_2, 2)

    expected_parsed_path_3 = [[DIR_NW, DIR_W, DIR_SW, DIR_E, DIR_E]]
    test_parse_paths(test_path_3, expected_parsed_path_3, 3)

    expected_parsed_path_4 = [[DIR_SE, DIR_SE, DIR_NW, DIR_NE, DIR_NE, DIR_NE, DIR_W, DIR_SE, DIR_E, DIR_SW, DIR_W,
                               DIR_SW, DIR_SW, DIR_W, DIR_NE, DIR_NE, DIR_W, DIR_SE, DIR_W, DIR_SW],
                              [DIR_NE, DIR_E, DIR_E, DIR_NE, DIR_SE, DIR_NW, DIR_NW, DIR_W, DIR_SW, DIR_NE, DIR_NE,
                               DIR_W, DIR_NW, DIR_W, DIR_SE, DIR_W, DIR_NE, DIR_NW, DIR_SE, DIR_SW, DIR_E, DIR_SW],
                              [DIR_SE, DIR_SW, DIR_NE, DIR_SW, DIR_SW, DIR_SE, DIR_NW, DIR_W, DIR_NW, DIR_SE],
                              [DIR_NW, DIR_NW, DIR_NE, DIR_SE, DIR_E, DIR_SW, DIR_SW, DIR_NE, DIR_NE, DIR_W, DIR_NE,
                               DIR_SW, DIR_W, DIR_NE, DIR_W, DIR_SE, DIR_SW, DIR_NE, DIR_SE, DIR_E, DIR_NE],
                              [DIR_SW, DIR_W, DIR_E, DIR_SW, DIR_NE, DIR_SW, DIR_NE, DIR_NW, DIR_SE, DIR_W, DIR_NW,
                               DIR_NE, DIR_NE, DIR_SE, DIR_E, DIR_NW],
                              [DIR_E, DIR_E, DIR_SE, DIR_NW, DIR_SE, DIR_SW, DIR_SW, DIR_NE, DIR_NW, DIR_SW, DIR_NW,
                               DIR_NW, DIR_SE, DIR_W, DIR_W, DIR_NW, DIR_SE, DIR_NE],
                              [DIR_SE, DIR_W, DIR_NE, DIR_NE, DIR_NE, DIR_NE, DIR_SE, DIR_NW, DIR_SE, DIR_W, DIR_NE,
                               DIR_NW, DIR_W, DIR_W, DIR_SE],
                              [DIR_W, DIR_E, DIR_NW, DIR_W, DIR_W, DIR_E, DIR_SE, DIR_E, DIR_E, DIR_W, DIR_E, DIR_SW,
                               DIR_W, DIR_W, DIR_NW, DIR_W, DIR_E],
                              [DIR_W, DIR_SW, DIR_E, DIR_E, DIR_SE, DIR_NE, DIR_NE, DIR_W, DIR_NW, DIR_W, DIR_NW,
                               DIR_SE, DIR_NE, DIR_W, DIR_SE, DIR_NW, DIR_W, DIR_SE, DIR_SE, DIR_SE, DIR_NW, DIR_NE],
                              [DIR_NE, DIR_E, DIR_SW, DIR_SE, DIR_E, DIR_NW, DIR_W, DIR_SW, DIR_NW, DIR_SW, DIR_SW,
                               DIR_NW],
                              [DIR_NE, DIR_NW, DIR_SW, DIR_W, DIR_SE, DIR_W, DIR_SW, DIR_NE, DIR_NE, DIR_NE, DIR_W,
                               DIR_SE, DIR_NW, DIR_SE, DIR_NW, DIR_NE, DIR_SE, DIR_SE, DIR_NE, DIR_W],
                              [DIR_E, DIR_NE, DIR_W, DIR_NW, DIR_E, DIR_W, DIR_NE, DIR_SW, DIR_SE, DIR_W, DIR_NW,
                               DIR_SW, DIR_E, DIR_NW, DIR_E, DIR_SW, DIR_NE, DIR_NW, DIR_SE, DIR_NW, DIR_SW],
                              [DIR_SW, DIR_E, DIR_NE, DIR_SW, DIR_NE, DIR_SW, DIR_NE, DIR_NE, DIR_E, DIR_NW, DIR_NE,
                               DIR_W, DIR_E, DIR_NE, DIR_W, DIR_W, DIR_NE, DIR_SW, DIR_SW, DIR_NE, DIR_SE],
                              [DIR_SW, DIR_W, DIR_E, DIR_SE, DIR_NE, DIR_SE, DIR_W, DIR_E, DIR_NW, DIR_NE, DIR_SW,
                               DIR_NW, DIR_W, DIR_NE, DIR_SE, DIR_SW, DIR_W, DIR_NE],
                              [DIR_E, DIR_NE, DIR_SE, DIR_NW, DIR_SW, DIR_W, DIR_SW, DIR_NE, DIR_NE, DIR_SW, DIR_SE,
                               DIR_NW, DIR_NE, DIR_W, DIR_SW, DIR_SE, DIR_E, DIR_NW, DIR_SE, DIR_SE],
                              [DIR_W, DIR_NW, DIR_NE, DIR_SE, DIR_NE, DIR_SE, DIR_NE, DIR_NW, DIR_W, DIR_NE, DIR_NW,
                               DIR_SE, DIR_W, DIR_E, DIR_SE, DIR_W, DIR_SE, DIR_SE, DIR_SE, DIR_W],
                              [DIR_NE, DIR_NE, DIR_W, DIR_SW, DIR_NW, DIR_E, DIR_W, DIR_SW, DIR_NE, DIR_NE, DIR_SE,
                               DIR_NW, DIR_NE, DIR_SE, DIR_W, DIR_E, DIR_SW],
                              [DIR_E, DIR_NE, DIR_SW, DIR_NW, DIR_SW, DIR_NW, DIR_SE, DIR_NE, DIR_NW, DIR_NW, DIR_NW,
                               DIR_W, DIR_SE, DIR_E, DIR_SW, DIR_NE, DIR_E, DIR_W, DIR_SE, DIR_NE, DIR_SE],
                              [DIR_NE, DIR_SW, DIR_NW, DIR_E, DIR_W, DIR_NW, DIR_NW, DIR_SE, DIR_E, DIR_NW, DIR_SE,
                               DIR_E, DIR_SE, DIR_W, DIR_SE, DIR_NW, DIR_SW, DIR_E, DIR_E, DIR_W, DIR_E],
                              [DIR_W, DIR_SE, DIR_W, DIR_E, DIR_E, DIR_E, DIR_NW, DIR_NE, DIR_SE, DIR_NW, DIR_W, DIR_W,
                               DIR_SW, DIR_NE, DIR_W]]
    test_parse_paths(test_path_4, expected_parsed_path_4, 4)

    test_parsed_path_1 = parse_raw_paths(test_path_1)
    expected_tile_coordinates = (3, 0)
    test_tile_coordinates = calculate_tile_coordinates_hexagon(test_parsed_path_1[0])
    print('Testing calculate_tile_coordinates_hexagon',
          'RIGHT' if expected_tile_coordinates == test_tile_coordinates
          else f'WRONG!! Expected {expected_tile_coordinates} but was {test_tile_coordinates}')

    expected_map = {(3, 0): 0}
    test_the_map = flip_tiles(test_parsed_path_1, calculate_tile_coordinates_hexagon)
    print('Testing flip_tiles (1)',
          'RIGHT' if expected_map == test_the_map else f'WRONG!! Expected {expected_map} but was {test_the_map}')

    test_parsed_path_4 = parse_raw_paths(test_path_4)
    expected_map = {(-2, 2): 0, (-1, -3): 1, (-2, 3): 0, (1, -2): 1, (0, -2): 1, (-1, 0): 1, (-2, 0): 0, (-1, -1): 0,
                    (-2, 1): 0, (-1, -2): 1, (1, -3): 0, (1, 2): 0, (0, 0): 0, (2, 0): 0, (-2, -1): 0}
    test_the_map = flip_tiles(test_parsed_path_4, calculate_tile_coordinates_hexagon)
    print('Testing flip_tiles (2)',
          'RIGHT' if expected_map == test_the_map else f'WRONG!! Expected {expected_map} but was {test_the_map}')

    expected_n_blacks = 10
    test_n_blacks = count_black_tiles(test_the_map)
    print('Testing count_black_tiles,'
          'RIGHT' if expected_n_blacks == test_n_blacks
          else f'WRONG!! Expected {expected_n_blacks} but was {test_n_blacks}')

    # SOLVE PART 1
    sol_parsed_path = parse_raw_paths(sol_raw_paths)
    sol_the_map = flip_tiles(sol_parsed_path, calculate_tile_coordinates_hexagon)
    sol_n_blacks = count_black_tiles(sol_the_map)
    print(f'SOLUTION PART 1: {sol_n_blacks}')
    print()

    print('PART 2')
    # TEST PART 2
    expected_adjacent = [(1, 0), (-1, 0), (-1, -1), (0, -1), (-1, 1), (0, 1)]
    test_adjacent = calculate_adjacent_tiles((0, 0))
    print('Testing calculate_adjacent_tiles (1)',
          'RIGHT' if expected_adjacent == test_adjacent
          else f'WRONG!! Expected {expected_adjacent} but was {test_adjacent}')

    expected_adjacent = [(1, 1), (-1, 1), (0, 0), (1, 0), (0, 2), (1, 2)]
    test_adjacent = calculate_adjacent_tiles((0, 1))
    print('Testing calculate_adjacent_tiles (2)',
          'RIGHT' if expected_adjacent == test_adjacent
          else f'WRONG!! Expected {expected_adjacent} but was {test_adjacent}')

    expected_map_past_1_day = {(-1, 2): 1, (-3, 2): 1, (-3, 1): 1, (-3, 3): 0, (-2, 2): 0, (0, -3): 1, (-2, -3): 1,
                               (-1, -4): 1, (0, -4): 1, (-1, -3): 1, (-1, 3): 1, (-2, 4): 1, (-1, 4): 1, (-2, 3): 0,
                               (2, -2): 1, (0, -1): 0, (1, -1): 1, (1, -2): 1, (0, -2): 1, (-1, 1): 0, (-1, 0): 1,
                               (-3, 0): 1, (-3, -1): 0, (-2, 0): 0, (-1, -1): 0, (-2, 1): 0, (-2, -2): 1, (-1, -2): 0,
                               (2, -3): 1, (1, -4): 1, (2, -4): 1, (1, -3): 1, (2, 2): 1, (0, 2): 1, (0, 1): 0,
                               (1, 1): 0,
                               (0, 3): 1, (1, 3): 1, (1, 2): 1, (1, 0): 0, (0, 0): 0, (3, 0): 1, (2, -1): 1, (2, 1): 1,
                               (2, 0): 1, (-2, -1): 0}
    test_map_past_1_day, _ = pass_day(test_the_map)
    print('Testing pass_day',
          'RIGHT' if expected_map_past_1_day == test_map_past_1_day
          else f'WRONG!! Expected {expected_map_past_1_day} but was {test_map_past_1_day}')

    expected_black_tiles_per_day = [(1, 15), (2, 12), (3, 25), (4, 14), (5, 23), (6, 28), (7, 41), (8, 37), (9, 49),
                                    (10, 37), (20, 132), (30, 259), (40, 406), (50, 566), (60, 788), (70, 1106),
                                    (80, 1373), (90, 1844), (100, 2208)]
    sample_days = list(range(1, 10)) + list(range(10, 101, 10))
    foo, sample_results = pass_days(test_the_map, 100, sample_days=sample_days)
    print('Testing pass_days',
          'RIGHT' if expected_black_tiles_per_day == sample_results
          else f'WRONG!! Expected {expected_black_tiles_per_day} but was {sample_results}')

    # SOLVE PART 2
    foo, _ = pass_days(sol_the_map, 100)
    n_blacks = count_black_tiles(foo)
    print('SOLUTION PART 2: ', n_blacks)
