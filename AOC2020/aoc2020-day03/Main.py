# DAY 3
import numpy as np
import re


# Utility functions. Load and validate maps
def check_map_is_valid(string_map):
    """
    Checks if the map has any rows and columns and if all rows are the same length.

    :param string_map: The map under testing.
    :return: True if map is valid, false otherwise.
    """
    # Map must have one line, at least
    if len(string_map) == 0:
        return False
    # First line must have columns
    width = len(string_map[0])
    if width == 0:
        return False

    # All lines must have same length
    for num_line in range(1, len(string_map)):
        if len(string_map[num_line]) != width:
            return False
    return True


def load_map(string_map):
    """
    Gets an string_map (array of strings) and converts it into a numpy bidimensional array of int values. The string_map
    will be validated prior transformation.

    :param string_map: The map to be loaded.
    :return: a numpy bidimensional array.
    """
    assert check_map_is_valid(string_map), 'Map is not valid!'

    height = len(string_map)
    width = len(string_map[0])

    # Initializing zero-matrix and filling with one when a
    # tree is found
    int_map = np.zeros([height, width], dtype=np.int)
    for num_line in range(height):
        line = string_map[num_line]
        for num_col in range(width):
            tree = line[num_col:num_col + 1]
            if tree == '#':
                int_map[num_line][num_col] = 1

    return int_map


# PART 1
def look_at(int_map, xpos, ypos, slope_x, slope_y):
    """
    Given an int_map it looks from (xpos, ypos), coordinates in (slope_x, slope_y) direction and returns everything it
    gets in the way.

    :param int_map: The map where action takes place.
    :param xpos: X coordinate of observer.
    :param ypos: Y coordinate of observer.
    :param slope_x: X component of the looking direction.
    :param slope_y: Y componnen of the looking direction.
    :return: List of tuple (a, b, c) beeing a and b coordinates and c what was at those coordinates.
    """

    # This is the height and it will be used to stop searching.
    max_y = len(int_map)
    # This is the width of the map. To simulate an infinite forest, we'll use this as modulus to be cycling around the
    # map, as it is always repeating itself, as we increase x coordinate.
    max_x = len(int_map[0])
    actual_x, actual_y = xpos, ypos

    objects = []
    while actual_y < max_y:
        actual_x += slope_x
        actual_y += slope_y

        # Although we always take an step (i.e. increase coordinates) we only look at the map if we are actually inside
        # the map. Notice we don't care about x coordinate as we always consider ourselves inside the map as it is an
        # infinite forest x axis wise.
        if actual_y < max_y:
            objects.append( (actual_x, actual_y, int_map[actual_y][actual_x % max_x] ))
    return objects


def count_trees(ray_result):
    """
    Counts how many trees are on a sample taken by look_at

    :param ray_result: Sample
    :return: number of trees
    """
    cnt = 0
    for (x, y, obj) in ray_result:
        if obj == 1:
            cnt += 1
    return cnt


if __name__ == '__main__':
    with open('data/aoc2020-input-day03.txt', 'r') as f:
        sol_str_map = [re.sub("\n", "", l) for l in f.readlines()]

    # TEST PART 1
    str_map = ['..##.......',
               '#...#...#..',
               '.#....#..#.',
               '..#.#...#.#',
               '.#...##..#.',
               '..#.##.....',
               '.#.#.#....#',
               '.#........#',
               '#.##...#...',
               '#...##....#',
               '.#..#...#.#']

    print(f'The map is {"RIGHT" if check_map_is_valid(str_map) else "WRONG"}')
    the_map = load_map(str_map)
    print(the_map)
    test_number_trees = count_trees(look_at(the_map, 0, 0, 3, 1))
    print('look_at is', 'RIGHT' if test_number_trees == 7 else f'WRONG, was {test_number_trees} expected 7')

    # SOLVE PART 1
    sol_map = load_map(sol_str_map)
    sol_result = look_at(sol_map, 0, 0, 3, 1)
    # print(sol_result)
    print('PART 1 SOLUTION', count_trees(sol_result))

    # TEST PART 2
    cnt = 1
    for x, y in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        cnt *= count_trees(look_at(the_map, 0, 0, x, y))
    print('Test Part 2 is', 'RIGHT' if cnt == 336 else f'WRONG, was {cnt} expected 336')

    #SOLVE PART 2
    cnt = 1
    for x, y in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        cnt *= count_trees(look_at(sol_map, 0, 0, x, y))

    print('PART 2 SOLUTION', cnt)
