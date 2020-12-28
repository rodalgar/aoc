# Day 20: Jurassic Jigsaw
import re
import math
import numpy as np
import functools
import operator


# PART 1
class Tile:
    tile_id = None
    raw = None
    actual_raw = None
    top_side = None
    bottom_side = None
    right_side = None
    left_side = None

    def __init__(self, tile_id):
        self.tile_id = tile_id
        self.raw = []
        self.actual_raw = []
        self.top_side = []
        self.bottom_side = []
        self.right_side = []
        self.left_side = []

    def __repr__(self):
        return f'\nid {self.tile_id} top {self.top_side} right {self.right_side} ' \
               f'bottom {self.bottom_side} left {self.left_side} '

    def print_tile(self):
        for row in self.actual_raw:
            print(row)

    def calculate_boundaries(self):
        """
        Calculates and stores the four lateral boundaries of the raw tile in the *_side properties of the instance.
        """
        self.top_side = self.actual_raw[0]
        self.bottom_side = self.actual_raw[-1]

        self.left_side = ''
        self.right_side = ''
        for h in range(len(self.actual_raw)):
            self.left_side += self.actual_raw[len(self.actual_raw) - h - 1][0]
            self.right_side += self.actual_raw[len(self.actual_raw) - h - 1][len(self.actual_raw[0]) - 1]

    @staticmethod
    def rotate_right(original):
        """
        Given an instance of Tile, returns another instance that has its actual raw image rotated 90º to the right. It
        has the same tile_id and raw image as the original. The boundaries of the new instance are calculated as well.

        :param original: The original tile to be rotated.
        :return: A new Tile object.
        """

        rotated_tile = Tile(original.tile_id)
        rotated_tile.raw = original.raw
        rotated_tile.actual_raw = []

        for w in range(len(original.actual_raw[0])):
            tmp_string = ''
            for h in range(len(original.actual_raw)):
                tmp_string += original.actual_raw[len(original.actual_raw) - h - 1][w]
            rotated_tile.actual_raw.append(tmp_string)

        rotated_tile.calculate_boundaries()

        return rotated_tile

    @staticmethod
    def vertical_flip(original):
        """
        Given an instance of Tile, returns another instance that has its actual raw image flipped vertically. It has
        the same tile_id and raw image as the original. The boundaries of the new instance are calculated as well.

        :param original: The original tile to be flipped.
        :return: A new Tile object.
        """

        flipped_tile = Tile(original.tile_id)
        flipped_tile.raw = original.raw
        flipped_tile.actual_raw = []

        for h in range(len(original.actual_raw)):
            flipped_tile.actual_raw.append(original.actual_raw[len(original.actual_raw) - h - 1])

        flipped_tile.calculate_boundaries()

        return flipped_tile

    @staticmethod
    def crop(original, crop_size):
        """
        Given an instance of Tile, returns another instance that has its borders cropped by the amount passed in the
        second parameter. It has the same tile_id and raw image as the original. The boundaries of the new instance are
        calculated as well.

        :param original: The original tile to be cropped.
        :param crop_size: How many rows and columns to crop.
        :return: A new Tile object.
        """

        cropped_tile = Tile(original.tile_id)
        cropped_tile.raw = original.raw
        cropped_tile.actual_raw = []

        for h in range(crop_size, len(original.actual_raw) - crop_size):
            cropped_tile.actual_raw.append(original.actual_raw[h][crop_size:len(original.actual_raw[0]) - crop_size])

        cropped_tile.calculate_boundaries()

        return cropped_tile

    @staticmethod
    def horizontal_merge(left, right):
        """
        Given two instances of Tile, returns another instance that is the horizontal merge of the two. It has no raw
        data anymore and the tile_id is the combined tile_ids of the originals. Boundaries are calculated as well.

        :param left: Original tile to be placed on the left side of the merge.
        :param right: Original tile to be placed on the right side of the merge.
        :return: A new Tile object.
        """

        assert len(left.actual_raw) == len(right.actual_raw), \
            f'Both tiles must be the same height L {len(left.actual_raw)} R {len(right.actual_raw)}'
        merged_tile = Tile(f'({left.tile_id}-{right.tile_id})')
        # No raw
        merged_tile.actual_raw = []

        for h in range(len(left.actual_raw)):
            merged_tile.actual_raw.append(left.actual_raw[h] + right.actual_raw[h])

        # Not necessary but for the sake of completeness
        merged_tile.calculate_boundaries()

        return merged_tile

    @staticmethod
    def vertical_merge(top, bottom):
        """
        Given two instances of Tile, returns another instance that is the vertical merge of the two. It has no raw data
        anymore and the tile_id is the combined tile_ids of the originals. Boundaries are calculated as well.

        :param top: Original tile to be placed on top of the merge.
        :param bottom: Original tile to be placed on the bottom side of the merge.
        :return: A new tile object.
        """
        assert len(top.actual_raw[0]) == len(bottom.actual_raw[0]), \
            f'Both tiles must be the same width T {len(top.actual_raw)} B {len(bottom.actual_raw)}'
        merged_tile = Tile(f'({top.tile_id}|{bottom.tile_id})')
        # No raw
        merged_tile.actual_raw = top.actual_raw[:]

        for row in bottom.actual_raw:
            merged_tile.actual_raw.append(row[:])

        # Not necessary but for the sake of completeness
        merged_tile.calculate_boundaries()

        return merged_tile


def parse_puzzle(raw_input):
    """
    Parses a string representing a tile set into a parsed puzzle.

    :param raw_input: string representing a puzzle
    :return: Parsed puzzle.
    """
    current_tile = None
    tiles = []
    for line in raw_input:
        if len(line) == 0:
            continue

        if line.startswith('Tile'):
            tile_id = re.findall("^Tile ([^:]+):", line)[0]
            current_tile = Tile(int(tile_id))
            tiles.append(current_tile)
        else:
            current_tile.raw.append(line)

    # Done reading
    for t in tiles:
        t.actual_raw = t.raw
        t.calculate_boundaries()

    return tiles


def get_transformed_tiles(original_tile_set):
    """
    Given a tile set (list of Tile) returns a new tile set in which all tiles are transformations of the originals. The
    transformations being applied are: Rotation to left and vertical flip.

    :param original_tile_set: List of Tile to be transformed.
    :return: List of Tile, containing transformations of the original tile set.
    """

    new_tiles = []
    for tile in original_tile_set:
        new_tiles.append(Tile.vertical_flip(tile))
        rotated = Tile.rotate_right(tile)
        for i in range(3):
            new_tiles.append(rotated)
            new_tiles.append(Tile.vertical_flip(rotated))
            rotated = Tile.rotate_right(rotated)

    return new_tiles


def get_eligible_tiles(puzzle, global_index, tile_set, max_width, verbose=False):
    """
    Given a puzzle state and coordinates (global index), gets a list of tiles that can be placed at said coordinates.
    Rules are that tiles should be yet unused and boundaries should match.

    :param puzzle: Puzzle state (numpy 1-Dimensional array)
    :param global_index: Index of puzzle. Coordinates.
    :param tile_set: tile set of puzzle.
    :param max_width: Width of the puzzle.
    :param verbose: If True additional info will be printed.
    :return: List of Tile that can be placed at coordinates.
    """

    # Get the used tiles first.
    used_tile_ids = [tile_set[puzzle[i]].tile_id for i in range(len(puzzle)) if puzzle[i] > 0]
    h, w = transform_global_index(global_index, max_width)
    if verbose:
        print(f'get_eligible_tiles. from global_index {global_index} h{h} w{w} used tile ids; {used_tile_ids}')

    # Filter tiles and get the unused ones. Notice that all transformations of an original tile share the same tile_id
    # (on purpose) so, when we chose one 'version' of the tile, the rest count as used as well and are not eligible. If
    # that 'version' is not fit to be at current coordinates, the next transformation is tried.
    eligible = [(ix, tile) for (ix, tile) in tile_set.items() if tile.tile_id not in used_tile_ids]

    # Now check boundaries
    # if row > 0. must match with above tile
    if h > 0:
        index_of_above_tile = transform_coordinates(h - 1, w, max_width)
        above_tile = tile_set[puzzle[index_of_above_tile]]
        eligible = [(ix, tile) for (ix, tile) in eligible if tile.top_side == above_tile.bottom_side]
    # if col > 0. must match with left tile
    if w > 0:
        left_tile = tile_set[puzzle[transform_coordinates(h, w - 1, max_width)]]
        eligible = [(ix, tile) for (ix, tile) in eligible if tile.left_side == left_tile.right_side]
    return eligible


def transform_coordinates(row, col, max_width):
    """
    Transforms a set of 2-D coordinates into a 1-D coordinate.

    :param row: Row component.
    :param col: Col component.
    :param max_width: Max length of the puzzle.
    :return: 1-D coordinate.
    """
    return (row * max_width) + col


def transform_global_index(global_index, max_width):
    """
    Transforms a 1-D coordinate into a pair of 2-D coodinates.

    :param global_index: 1-D coordinate.
    :param max_width: Max length of the puzzle.
    :return: Tuple row, col
    """
    row = global_index // max_width
    col = global_index % max_width
    return row, col


def try_tile(puzzle, global_index, tile_set, max_width, level=0, verbose=False):
    """
    Recursively tries each tile of the tile set in each position.

    :param puzzle: Puzzle state.
    :param global_index: Coordinate being tested.
    :param tile_set: Set of all tiles in the puzzle (plus its transformations...)
    :param max_width: max width of the puzzle.
    :param level: keeps track of which level of recursion we are in. As we treat only one coordinate per recursion level
    this is very similar to the number of tile we are currently processing.
    :param verbose: If True additional info will be printed.
    :return: tuple of x, y, being x whether or not the puzzle was solved and the solved puzzle (or None if it couldn't
    be solved)
    """

    # If we reach the last tile, the puzzle was successfully completed. Yay!
    if level == len(puzzle):
        return True, puzzle

    if verbose:
        print(f'Level {level}, global_index {global_index}, puzzle {puzzle}')

    # We get which tiles can be placed in this coordinate, and try them one at a time.
    eligible_tiles = get_eligible_tiles(puzzle, global_index, tile_set, max_width, verbose)
    if verbose:
        print('try_tile', 'eligible are', eligible_tiles)

    for eligible_tile in eligible_tiles:
        if verbose:
            print(f'eligible tile to process {eligible_tile}')
        ix, tile = eligible_tile
        puzzle[global_index] = ix
        if verbose:
            print(f'This is how the puzzle looks with the eligible tile placed: {puzzle}')

        # With the eligible tile placed, we try to solve the puzzle. If it can be solved, we are finished. If not we
        # place another of the eligible tiles instead and try to solve. If it can't be solved with any of the eligible
        # tiles we'll return False so our caller know that it should try another tile.
        for new_global_index in range(global_index, len(puzzle)):
            new_global_index += 1

            result, new_puzzle = try_tile(puzzle, new_global_index, tile_set, max_width, level + 1, verbose=verbose)
            if result:
                return True, new_puzzle
            else:
                break

    # If there are no eligible tiles or any of them can't be placed (or lead to a solution) it means this puzzle state
    # is not useful.. probably the last tile added should be removed and tried elsewhere.
    return False, None


def fun_with_puzzles(original_tile_set, verbose=False):
    """
    Solves the puzzle. First it calculates an 'extended tile set' that contains the original tile set plus its meaning
    transformations (ie. rotation to the right and vertical flip). Then it tries all the tiles in order.

    :param original_tile_set: Original set of tiles.
    :param verbose: If True additional info will be printed.
    :return: Solved puzzle, list of tile_id of the corners
    """

    # Tiles are squared so, as the puzzle is also square shaped, that means the same tiles are on the h-axis and the
    # w-axis.
    length_of_puzzle = int(math.sqrt(len(original_tile_set)))

    if verbose:
        print(f'length of puzzle is {length_of_puzzle}')

    # We make a new tile set putting together the original tile set and another one created with every possible
    # transformation. Rotating, vertical flip, horizontal flip. Just a note. Not all transformations are required as
    # performing and horizontal flip will yield the same result as performing rotations and vertical flips. The same
    # goes to performing an horizontal and vertical flip. So, in the end, only rotations and vertical flips are needed.
    transformed_tile_set = {i + 1: v for i, v in
                            enumerate(original_tile_set + get_transformed_tiles(original_tile_set))}

    if verbose:
        print(f'Transformed puzzle has {len(transformed_tile_set)} tiles')

    # Initializing the puzzle as 1-Dimensional array.
    puzzle = np.zeros(shape=(length_of_puzzle * length_of_puzzle), dtype=int)

    # Beginning a recursive process from the first tile of the puzzle.
    result, puzzle = try_tile(puzzle, 0, transformed_tile_set, length_of_puzzle, verbose)

    if verbose:
        print('Final result: ')
        print(result, puzzle)

    # now we get the four corners:
    corners = [transformed_tile_set[puzzle[transform_coordinates(0, 0, length_of_puzzle)]].tile_id,
               transformed_tile_set[puzzle[transform_coordinates(0, length_of_puzzle - 1, length_of_puzzle)]].tile_id,
               transformed_tile_set[puzzle[transform_coordinates(length_of_puzzle - 1, 0, length_of_puzzle)]].tile_id,
               transformed_tile_set[puzzle[transform_coordinates(length_of_puzzle - 1, length_of_puzzle - 1,
                                                                 length_of_puzzle)]].tile_id]

    # Tiles really used to solve the puzzle. This is because the transformed tile set is something made-up in this
    # function so, external consumers need to know the final shape of the tiles. We could also make another structure
    # with only the raw symbols.
    used_tile_set = {k: v for k, v in transformed_tile_set.items() if k in puzzle}

    return corners, puzzle, used_tile_set


def solve_part_1(corners):
    """
    Calculates the product of the elements of an array.

    :param corners: The array.
    :return: The product of the elements.
    """
    return functools.reduce(operator.mul, corners)


# PART 2
def get_complete_habitat_image(solved_puzzle, used_tile_set, verbose=False):
    """
    Gets a complete image based into the solved puzzle passed. It removes the borders of the tiles and then merges them
    into a great tile.

    :param solved_puzzle: Solved puzzle to merge.
    :param used_tile_set: set of tiles of the puzzle.
    :param verbose: If True additional info will be printed.
    :return: A Tile object with all tiles of the original puzzle merged.
    """

    # Generate a new tile set like the other but with trimmed borders.
    cropped_tile_set = {k: Tile.crop(v, 1) for k, v in used_tile_set.items()}
    puzzle_len = int(math.sqrt(solved_puzzle.shape[0]))
    if verbose:
        print(cropped_tile_set)

    # Merge all tile in the same row to form rows of only 1 column long.
    merged_tiles = []
    for h in range(puzzle_len):
        merged_tiles.append(cropped_tile_set[solved_puzzle[transform_coordinates(h, 0, max_width=puzzle_len)]])
        for c in range(1, puzzle_len):
            merged_tiles[h] = Tile.horizontal_merge(merged_tiles[h],
                                                    cropped_tile_set[solved_puzzle[transform_coordinates(h,
                                                                                                         c,
                                                                                                         puzzle_len)]])

    # Merge all rows to form a 1 cell tile set
    merged_tile = merged_tiles[0]
    for h in range(1, len(merged_tiles)):
        merged_tile = Tile.vertical_merge(merged_tile, merged_tiles[h])

    if verbose:
        print(merged_tile)
        print(merged_tile.actual_raw)

    return merged_tile


def scan_habitat_for_monster(habitat_to_scan, monster, verbose=False):
    """
    Given a tile representing an habitat and a monster pattern finds all occurrences of the monster pattern and marks
    them in the map.

    :param habitat_to_scan: Tile representing the habitat to scan.
    :param monster: Pattern of the monster.
    :param verbose: If True additional info will be printed.
    :return: List of tuple with coordinates of monster sightings and a copy of the original habitat in which all the
    sea monsters positions are marked.
    """

    # Transform the pattern of the monster into a regexp.
    monster_pattern = ''.join(monster).replace(" ", r".")
    monster_pattern = re.sub(r'(\.+)', r'(\1)', monster_pattern)
    window_size = len(monster[0])

    # Make 3-line groups into a line to search the monster pattern unto.
    monster_sightings = []
    for h in range(2, len(habitat_to_scan.actual_raw)):
        for c in range(len(habitat_to_scan.actual_raw[0]) - window_size - 1):
            habitat_pattern = habitat_to_scan.actual_raw[h - 2][c:window_size + c] \
                              + habitat_to_scan.actual_raw[h - 1][c:window_size + c] \
                              + habitat_to_scan.actual_raw[h][c:window_size + c]
            result = re.search(monster_pattern, habitat_pattern)

            if result is not None:
                if verbose:
                    print(f'THAR IT BLOWS!!! at h {h} c {c}')
                monster_sightings.append((h, c))

    # For each sighting, we will mark the monster on the map.
    for h, c in monster_sightings:
        habitat_pattern = habitat_to_scan.actual_raw[h - 2][c:window_size + c] \
                          + habitat_to_scan.actual_raw[h - 1][c:window_size + c] \
                          + habitat_to_scan.actual_raw[h][c:window_size + c]
        habitat_pattern_with_monster = re.sub(monster_pattern, r'\1O\2O\3OO\4OO\5OOO\6O\7O\8O\9O\10O\11O\12',
                                              habitat_pattern)
        for offset in range(3):
            whole_line = habitat_to_scan.actual_raw[h - offset]
            new_line = whole_line[:c] \
                       + habitat_pattern_with_monster[(2 - offset) * window_size
                                                      :(2 - offset) * window_size + window_size] \
                       + whole_line[c + window_size:]
            habitat_to_scan.actual_raw[h - offset] = new_line

    return monster_sightings, habitat_to_scan


def pinpoint_sea_monsters(original_habitat, monster, verbose=False):
    """
    Given a mega Tile representing and habitat, we look for monsters trying some transformations (as with some other
    functions, we only need rotation to right and vertical flip).

    :param original_habitat: Original Tile in which to perform the search.
    :param monster: Monster pattern to look for.
    :param verbose: If True additional info will be printed.
    :return: The final (possibly transformed) Tile with all sea monsters marked. And a list of coordinates of the
    sightings.
    """
    if verbose:
        print(f'habitat.actual_raw {len(original_habitat.actual_raw)}')
    rotated_tile = original_habitat
    final_habitat = None
    sightings = None

    # Test all transformations of input habitat to see in which one there be dragons er.. sea monsters.
    # Same as part 1 (ie. Only rotation to right and vertical flip needed)
    for i in range(4):
        sightings, scanned_habitat = scan_habitat_for_monster(rotated_tile, monster, verbose)

        if len(sightings) > 0:
            final_habitat = scanned_habitat
            break
        else:
            flipped_habitat = Tile.vertical_flip(rotated_tile)
            sightings, scanned_habitat = scan_habitat_for_monster(flipped_habitat, monster, verbose)
            if len(sightings) > 0:
                final_habitat = scanned_habitat
                break

        rotated_tile = Tile.rotate_right(rotated_tile)

    if verbose:
        if final_habitat is not None:
            print('Found the beasts.')
        else:
            print('No sea monsters?')

    return final_habitat, sightings


def solve_part_2(habitat_with_monsters):
    """
    Calculates how many # symbols are contained in the habitat.
    :param habitat_with_monsters: Habitat to count # symbols in.
    :return: Number of # symbols.
    """
    return sum(map(lambda x: x.count('#'), habitat_with_monsters.actual_raw))


if __name__ == '__main__':
    with open('data/aoc2020-input-day20.txt', 'r') as f:
        sol_raw_puzzle = [line.strip('\n') for line in f.readlines()]

    test_raw_puzzle_1 = ['Tile 2311:',
                         '..##.#..#.',
                         '##..#.....',
                         '#...##..#.',
                         '####.#...#',
                         '##.##.###.',
                         '##...#.###',
                         '.#.#.#..##',
                         '..#....#..',
                         '###...#.#.',
                         '..###..###',
                         '',
                         'Tile 1951:',
                         '#.##...##.',
                         '#.####...#',
                         '.....#..##',
                         '#...######',
                         '.##.#....#',
                         '.###.#####',
                         '###.##.##.',
                         '.###....#.',
                         '..#.#..#.#',
                         '#...##.#..',
                         '',
                         'Tile 1171:',
                         '####...##.',
                         '#..##.#..#',
                         '##.#..#.#.',
                         '.###.####.',
                         '..###.####',
                         '.##....##.',
                         '.#...####.',
                         '#.##.####.',
                         '####..#...',
                         '.....##...',
                         '',
                         'Tile 1427:',
                         '###.##.#..',
                         '.#..#.##..',
                         '.#.##.#..#',
                         '#.#.#.##.#',
                         '....#...##',
                         '...##..##.',
                         '...#.#####',
                         '.#.####.#.',
                         '..#..###.#',
                         '..##.#..#.',
                         '',
                         'Tile 1489:',
                         '##.#.#....',
                         '..##...#..',
                         '.##..##...',
                         '..#...#...',
                         '#####...#.',
                         '#..#.#.#.#',
                         '...#.#.#..',
                         '##.#...##.',
                         '..##.##.##',
                         '###.##.#..',
                         '',
                         'Tile 2473:',
                         '#....####.',
                         '#..#.##...',
                         '#.##..#...',
                         '######.#.#',
                         '.#...#.#.#',
                         '.#########',
                         '.###.#..#.',
                         '########.#',
                         '##...##.#.',
                         '..###.#.#.',
                         '',
                         'Tile 2971:',
                         '..#.#....#',
                         '#...###...',
                         '#.#.###...',
                         '##.##..#..',
                         '.#####..##',
                         '.#..####.#',
                         '#..#.#..#.',
                         '..####.###',
                         '..#.#.###.',
                         '...#.#.#.#',
                         '',
                         'Tile 2729:',
                         '...#.#.#.#',
                         '####.#....',
                         '..#.#.....',
                         '....#..#.#',
                         '.##..##.#.',
                         '.#.####...',
                         '####.#.#..',
                         '##.####...',
                         '##..#.##..',
                         '#.##...##.',
                         '',
                         'Tile 3079:',
                         '#.#.#####.',
                         '.#..######',
                         '..#.......',
                         '######....',
                         '####.#..#.',
                         '.#...#.##.',
                         '#.#####.##',
                         '..#.###...',
                         '..#.......',
                         '..#.###...']

    test_raw_tile_1 = ['Tile 2311:',
                       '..##.#..#.',
                       '##..#.....',
                       '#...##..#.',
                       '####.#...#',
                       '##.##.###.',
                       '##...#.###',
                       '.#.#.#..##',
                       '..#....#..',
                       '###...#.#.',
                       '..###..###']

    test_raw_habitat_1 = ['.#.#..#.##...#.##..#####',
                          '###....#.#....#..#......',
                          '##.##.###.#.#..######...',
                          '###.#####...#.#####.#..#',
                          '##.#....#.##.####...#.##',
                          '...########.#....#####.#',
                          '....#..#...##..#.#.###..',
                          '.####...#..#.....#......',
                          '#..#.##..#..###.#.##....',
                          '#.####..#.####.#.#.###..',
                          '###.#.#...#.######.#..##',
                          '#.####....##..########.#',
                          '##..##.#...#...#.#.#.#..',
                          '...#..#..#.#.##..###.###',
                          '.#.#....#.##.#...###.##.',
                          '###.#...#..#.##.######..',
                          '.#.#.###.##.##.#..#.##..',
                          '.####.###.#...###.#..#.#',
                          '..#.#..#..#.#.#.####.###',
                          '#..####...#.#.#.###.###.',
                          '#####..#####...###....##',
                          '#.##..#..#...#..####...#',
                          '.#.###..##..##..####.##.',
                          '...###...##...#...#..###']

    test_raw_habitat_2 = ['.####...#####..#...###..',
                          '#####..#..#.#.####..#.#.',
                          '.#.#...#.###...#.##.##..',
                          '#.#.##.###.#.##.##.#####',
                          '..##.###.####..#.####.##',
                          '...#.#..##.##...#..#..##',
                          '#.##.#..#.#..#..##.#.#..',
                          '.###.##.....#...###.#...',
                          '#.####.#.#....##.#..#.#.',
                          '##...#..#....#..#...####',
                          '..#.##...###..#.#####..#',
                          '....#.##.#.#####....#...',
                          '..##.##.###.....#.##..#.',
                          '#...#...###..####....##.',
                          '.#.##...#.##.#.#.###...#',
                          '#.###.#..####...##..#...',
                          '#.###...#.##...#.######.',
                          '.###.###.#######..#####.',
                          '..##.#..#..#.#######.###',
                          '#.#..##.########..#..##.',
                          '#.#####..#.#...##..#....',
                          '#....##..#.#########..##',
                          '#...#.....#..##...###.##',
                          '#..###....##.#...##.##.#']

    print('PART 1')
    # TEST PART 1
    expected_parsed_tile = ['..##.#..#.', '##..#.....', '#...##..#.', '####.#...#', '##.##.###.', '##...#.###',
                            '.#.#.#..##', '..#....#..', '###...#.#.', '..###..###']
    test_tile_1 = parse_puzzle(test_raw_tile_1)
    test_tile = test_tile_1[0]
    print('Testing parse_puzzle (1)',
          'RIGHT' if len(test_tile_1) == 1 else f'WRONG!! Expected 1 but was {len(test_tile_1)}')
    print('Testing parse_puzzle (tile_id)',
          'RIGHT' if test_tile.tile_id == 2311 else f'WRONG!! Expected 2311 but was {test_tile.tile_id}')
    print('Testing parse_puzzle (tile shape)',
          'RIGHT' if test_tile.actual_raw == expected_parsed_tile
          else f'WRONG!! Expected {expected_parsed_tile} but was {test_tile.actual_raw}')
    test_puzzle_1 = parse_puzzle(test_raw_puzzle_1)
    print('Testing parse_puzzle (2)',
          'RIGHT' if len(test_puzzle_1) == 9 else f'Expected 9 tiles but was {len(test_puzzle_1)}')

    expected_rotated_tile = ['.#..#####.', '.#.####.#.', '###...#..#', '#..#.##..#', '#....#.##.', '...##.##.#',
                             '.#...#....', '#.#.##....', '##.###.#.#', '#..##.#...']
    test_tile = Tile.rotate_right(test_tile)
    print('Testing Tile.rotate_right',
          'RIGHT' if test_tile.actual_raw == expected_rotated_tile
          else f'WRONG!! Expected {expected_rotated_tile} but was {test_tile.actual_raw}')
    expected_flipped_tile = ['#..##.#...', '##.###.#.#', '#.#.##....', '.#...#....', '...##.##.#', '#....#.##.',
                             '#..#.##..#', '###...#..#', '.#.####.#.', '.#..#####.']
    test_tile = Tile.vertical_flip(test_tile)
    print('Testing Tile.vertical_flip',
          'RIGHT' if test_tile.actual_raw == expected_flipped_tile
          else f'WRONG!! Expected {expected_flipped_tile} but was {test_tile.actual_raw}')

    expected_tile_id_corners = [2971, 1171, 1951, 3079]
    test_corners, test_solved_puzzle, test_used_tile_set = fun_with_puzzles(test_puzzle_1)
    print('Testing fun_with_puzzles',
          'RIGHT' if test_corners == expected_tile_id_corners
          else f'WRONG!! Expected {expected_tile_id_corners} but was {test_corners}')
    expected_result_test = 20899048083289
    result_test_1 = solve_part_1(test_corners)
    print('Testing solve_part_1',
          'RIGHT' if result_test_1 == expected_result_test
          else f'WRONG!! Expected {expected_result_test} but was {result_test_1}')

    # SOLVE PART 1
    sol_puzzle = parse_puzzle(sol_raw_puzzle)
    sol_corners, sol_solved_puzzle, sol_used_tile_set = fun_with_puzzles(sol_puzzle)
    print('SOLUTION PART 1', solve_part_1(sol_corners))
    print()

    print('PART 2')
    # TEST PART 2
    expected_cropped_tile = ['#.##..', '...#..', '.##.##', '...#.#', '.#.##.', '#...#.']
    test_tile = Tile.crop(test_tile, 2)
    print('Testing Tile.crop',
          'RIGHT' if test_tile.actual_raw == expected_cropped_tile
          else f'WRONG!! Expected {expected_cropped_tile} but was {test_tile.actual_raw}')

    expected_horizontal_merge = ['#.##..#.##..', '...#.....#..', '.##.##.##.##',
                                 '...#.#...#.#', '.#.##..#.##.', '#...#.#...#.']
    foo = Tile.horizontal_merge(test_tile, test_tile)
    print('Testing Tile.horizontal_merge',
          'RIGHT' if foo.actual_raw == expected_horizontal_merge
          else f'WRONG!! Expected {expected_horizontal_merge} but was {foo.actual_raw}')

    expected_vertical_merge = ['#.##..', '...#..', '.##.##', '...#.#', '.#.##.', '#...#.',
                               '#.##..', '...#..', '.##.##', '...#.#', '.#.##.', '#...#.']
    foo = Tile.vertical_merge(test_tile, test_tile)
    print('Testing Tile.vertical_merge',
          'RIGHT' if foo.actual_raw == expected_vertical_merge
          else f'WRONG!! Expected {expected_vertical_merge} but was {foo.actual_raw}')

    expected_complete_habitat = ['...###...##...#...#..###', '.#.###..##..##..####.##.', '#.##..#..#...#..####...#',
                                 '#####..#####...###....##', '#..####...#.#.#.###.###.', '..#.#..#..#.#.#.####.###',
                                 '.####.###.#...###.#..#.#', '.#.#.###.##.##.#..#.##..', '###.#...#..#.##.######..',
                                 '.#.#....#.##.#...###.##.', '...#..#..#.#.##..###.###', '##..##.#...#...#.#.#.#..',
                                 '#.####....##..########.#', '###.#.#...#.######.#..##', '#.####..#.####.#.#.###..',
                                 '#..#.##..#..###.#.##....', '.####...#..#.....#......', '....#..#...##..#.#.###..',
                                 '...########.#....#####.#', '##.#....#.##.####...#.##', '###.#####...#.#####.#..#',
                                 '##.##.###.#.#..######...', '###....#.#....#..#......', '.#.#..#.##...#.##..#####']
    habitat = get_complete_habitat_image(test_solved_puzzle, test_used_tile_set)
    print('Test get_complete_habitat_image',
          'RIGHT' if habitat.actual_raw == expected_complete_habitat
          else f'WRONG!! Expected {expected_complete_habitat} but was {habitat.actual_raw}')

    sea_monster_shape = ['                  # ',
                         '#    ##    ##    ###',
                         ' #  #  #  #  #  #   ']

    test_tile_habitat_2 = Tile('test_habitat_well_oriented')
    test_tile_habitat_2.actual_raw = test_raw_habitat_2
    expected_marked_habitat = ['.####...#####..#...###..', '#####..#..#.#.####..#.#.', '.#.#...#.###...#.##.O#..',
                               '#.O.##.OO#.#.OO.##.OOO##', '..#O.#O#.O##O..O.#O##.##', '...#.#..##.##...#..#..##',
                               '#.##.#..#.#..#..##.#.#..', '.###.##.....#...###.#...', '#.####.#.#....##.#..#.#.',
                               '##...#..#....#..#...####', '..#.##...###..#.#####..#', '....#.##.#.#####....#...',
                               '..##.##.###.....#.##..#.', '#...#...###..####....##.', '.#.##...#.##.#.#.###...#',
                               '#.###.#..####...##..#...', '#.###...#.##...#.##O###.', '.O##.#OO.###OO##..OOO##.',
                               '..O#.O..O..O.#O##O##.###', '#.#..##.########..#..##.', '#.#####..#.#...##..#....',
                               '#....##..#.#########..##', '#...#.....#..##...###.##', '#..###....##.#...##.##.#']
    test_sightings, test_marked_habitat = scan_habitat_for_monster(test_tile_habitat_2, sea_monster_shape)
    print('Testing scan_habitat_for_monster, n_sights',
          'RIGHT' if len(test_sightings) == 2 else f'WRONG!! Expected 2 but was {len(test_sightings)}')
    print('Testing scan_habitat_for_monster, shape',
          'RIGHT' if test_marked_habitat.actual_raw == expected_marked_habitat
          else f'WRONG!! Expected {test_marked_habitat.actual_raw} but was {expected_marked_habitat}')

    test_tile_habitat_1 = Tile('test_habitat_bad_oriented')
    test_tile_habitat_1.actual_raw = test_raw_habitat_1

    test_habitat_with_monsters, test_sightings = pinpoint_sea_monsters(test_tile_habitat_1, sea_monster_shape)
    print('Testing pinpoint_sea_monsters, n_sights',
          'RIGHT' if len(test_sightings) == 2 else f'WRONG!! Expected 2 but was {len(test_sightings)}')
    print('Testing pinpoint_sea_monsters, shape',
          'RIGHT' if test_habitat_with_monsters.actual_raw == expected_marked_habitat
          else f'WRONG!! Expected {test_habitat_with_monsters.actual_raw} but was {expected_marked_habitat}')

    test_water_roughness = solve_part_2(test_habitat_with_monsters)
    print('Testing solve_part_2',
          'RIGHT' if test_water_roughness == 273 else f'WRONG!! Expected 273 but was {test_water_roughness}')

    # SOLVE PART 2
    sol_habitat = get_complete_habitat_image(sol_solved_puzzle, sol_used_tile_set)
    sol_habitat_with_monsters, sol_sightings = pinpoint_sea_monsters(sol_habitat, sea_monster_shape)

    print('SOLUTION PART 2', solve_part_2(sol_habitat_with_monsters))
