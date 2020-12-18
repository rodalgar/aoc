# Day 17: Conway Cubes


# PART 1
class Cube:
    isAlive = None
    isAliveInNextCycle = None
    neighbors = None
    id = None

    def __init__(self, isALive, i, j, k):
        self.isAlive = isALive
        self.neighbors = []
        self.id = f'{i},{j},{k}'

    def __repr__(self):
        return f'{"#" if self.isAlive else "."} {self.id} ({[n.id for n in self.neighbors]})'


def link_cubes(a, b):
    """
    Links two cubes by adding them to each other's neighbors list.

    :param a: cube a
    :param b: cube b
    """
    if b not in a.neighbors:
        a.neighbors.append(b)
    if a not in b.neighbors:
        b.neighbors.append(a)


def parse_map(raw_space):
    """
    Parses a list of string representing an space of cubes into a 3D space.

    :param raw_space: Raw space
    :return: Dictionary of Cubes, indexed by tuple of coordinates, and value a Cube with living status.
    """
    height = len(raw_space)
    width = len(raw_space[0])
    # input is 2-D, so we consider z-axis to be 0
    depth = 0

    int_sparse_map = {}
    for num_line in range(height):
        line = raw_space[num_line]
        for num_col in range(width):
            symbol = line[num_col:num_col + 1]
            int_sparse_map[(num_line, num_col, depth)] = Cube(symbol == '#', num_line, num_col, depth)

    # Adjacent
    map_adjacent_cubes = {}
    for (x, y, z), sq in int_sparse_map.items():
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if i == j == k == 0:
                        continue
                    n_cor = (x + i, y + j, z + k)
                    if n_cor in int_sparse_map:
                        n = int_sparse_map[n_cor]
                        sq.neighbors.append(n)
                    else:
                        if n_cor in map_adjacent_cubes:
                            n = map_adjacent_cubes[n_cor]
                            link_cubes(sq, n)
                        else:
                            n = Cube(False, x + i, y + j, z + k)
                            map_adjacent_cubes[n_cor] = n
                            link_cubes(sq, n)

    int_sparse_map.update(map_adjacent_cubes)

    return int_sparse_map


def expand(int_map, verbose=False):
    """
    Performs a cycle as per rules of part 1.

    :param int_map: Parsed map.
    :param verbose: If True additional info will be printed.
    :return: expanded map
    """
    int_map_out = {}

    # Change status for all reachable squares in this cycle
    for (x, y, z), sq in int_map.items():
        live_neighbors = list(filter(lambda x: x.isAlive, sq.neighbors))
        n_live_neighbors = len(live_neighbors)

        if sq.isAlive:
            if verbose:
                print(f'\tCube {sq.id}. ACTIVE. {n_live_neighbors} live neighbors. Alive: {2 <= n_live_neighbors <= 3}')
            sq.isAliveInNextCycle = 2 <= n_live_neighbors <= 3
        else:
            if verbose:
                print(f'\tCube {sq.id}. INACTIVE. {n_live_neighbors} live neighbors. Alive: {n_live_neighbors == 3}')
            sq.isAliveInNextCycle = n_live_neighbors == 3

        int_map_out[(x, y, z)] = sq

    # Update status and Weave next adjacent layer
    map_adjacent_cubes = {}
    for (x, y, z), sq in int_map_out.items():
        sq.isAlive = sq.isAliveInNextCycle

        # 26 neighbors: 3x3x3 - 1 (a cube is not a neighbor of itself)
        if len(sq.neighbors) != 26:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    for k in range(-1, 2):
                        if i == j == k == 0:
                            continue
                        n_cor = (x + i, y + j, z + k)
                        if n_cor in int_map_out:
                            n = int_map_out[n_cor]
                            link_cubes(sq, n)
                        else:
                            if n_cor in map_adjacent_cubes:
                                n = map_adjacent_cubes[n_cor]
                                link_cubes(sq, n)
                            else:
                                n = Cube(False, x + i, y + j, z + k)
                                map_adjacent_cubes[n_cor] = n
                                link_cubes(sq, n)

    int_map_out.update(map_adjacent_cubes)

    if verbose:
        print('Cubes after expanding', len(int_map_out))

    return int_map_out


def count_active_squares(int_map):
    """
    Counts how many living cubes are in a given map.

    :param int_map: Map to count living squares.
    :return: number of living squares.
    """
    return sum(map(lambda x: 1 if x.isAlive else 0, int_map.values()))


def cycle_map(int_map, number_cycles, fun_expand, verbose=False):
    """
    Expands a map 'number_cycles' times. 'fun_expand' is used to expand the map.

    :param int_map: Map to expand.
    :param number_cycles: Number of times to cycle map.
    :param fun_expand: Function used to expand the map.
    :param verbose: If True additional info will be printed.
    :return: number of living squares and last cycled map.
    """
    for c in range(number_cycles):
        int_map = fun_expand(int_map)
        l_squares = count_active_squares(int_map)
        if verbose:
            print(c, l_squares)

    return l_squares, int_map


# PART 2
class HyperCube(Cube):

    def __init__(self, isALive, i, j, k, w):
        super().__init__(isALive, i, j, k)
        self.id = f'{i},{j},{k},{w}'


def parse_map_v2(raw_space):
    """
    Parses a list of string representing an space of cubes into a 4D space.

    :param raw_space: Raw space
    :return: Dictionary of Cubes, indexed by tuple of coordinates, and value a Cube with living status.
    """

    height = len(raw_space)
    width = len(raw_space[0])
    # input is 2-D, so we consider z-axis to be 0
    depth = 0
    # input is 2-D so we consider w-axis to be 0
    time = 0

    int_sparse_map = {}
    for num_line in range(height):
        line = raw_space[num_line]
        for num_col in range(width):
            symbol = line[num_col:num_col + 1]
            int_sparse_map[(num_line, num_col, depth, time)] = HyperCube(symbol == '#', num_line, num_col, depth, time)

    # Adjacent
    map_adjacent_cubes = {}
    for (x, y, z, w), sq in int_sparse_map.items():
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if i == j == k == l == 0:
                            continue
                        n_cor = (x + i, y + j, z + k, w + l)
                        if n_cor in int_sparse_map:
                            n = int_sparse_map[n_cor]
                            sq.neighbors.append(n)
                        else:
                            if n_cor in map_adjacent_cubes:
                                n = map_adjacent_cubes[n_cor]
                                link_cubes(sq, n)
                            else:
                                n = HyperCube(False, x + i, y + j, z + k, w + l)
                                map_adjacent_cubes[n_cor] = n
                                link_cubes(sq, n)

    int_sparse_map.update(map_adjacent_cubes)

    return int_sparse_map


def expand_v2(int_map, verbose=False):
    """
    Performs a cycle as per rules of part 2.

    :param int_map: Parsed map.
    :param verbose: If True additional info will be printed.
    :return: expanded map.
    """

    int_map_out = {}

    # Change status for all reachable squares in this cycle
    for (x, y, z, w), sq in int_map.items():
        live_neighbors = list(filter(lambda x: x.isAlive, sq.neighbors))
        n_live_neighbors = len(live_neighbors)

        if sq.isAlive:
            if verbose:
                print(f'\tCube {sq.id}. ACTIVE. {n_live_neighbors} live neighbors. Alive: {2 <= n_live_neighbors <= 3}')
            sq.isAliveInNextCycle = 2 <= n_live_neighbors <= 3
        else:
            if verbose:
                print(f'\tCube {sq.id}. INACTIVE. {n_live_neighbors} live neighbors. Alive: {n_live_neighbors == 3}')
            sq.isAliveInNextCycle = n_live_neighbors == 3

        int_map_out[(x, y, z, w)] = sq

    # Update status and Weave next adjacent layer
    map_adjacent_cubes = {}
    for (x, y, z, w), sq in int_map_out.items():
        sq.isAlive = sq.isAliveInNextCycle

        # 80 neighbors: 3x3x3x3 - 1 (a cube is not a neighbor of itself)
        if len(sq.neighbors) != 80:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            if i == j == k == l == 0:
                                continue
                            n_cor = (x + i, y + j, z + k, w + l)
                            if n_cor in int_map_out:
                                n = int_map_out[n_cor]
                                link_cubes(sq, n)
                            else:
                                if n_cor in map_adjacent_cubes:
                                    n = map_adjacent_cubes[n_cor]
                                    link_cubes(sq, n)
                                else:
                                    n = HyperCube(False, x + i, y + j, z + k, w + l)
                                    map_adjacent_cubes[n_cor] = n
                                    link_cubes(sq, n)

    int_map_out.update(map_adjacent_cubes)

    if verbose:
        print('HyperCubes after expanding', len(int_map_out))

    return int_map_out


def test_cycle_map(test_ism, expected_layer_z_zero):
    """
    Function to test cycle_map. Comparing a calculated layer z=0 with an expected layer z

    :param test_ism: Cycled map to test.
    :param expected_layer_z_zero: Expected layer z
    """
    cubes_z_zero = {}
    for (x, y, z), sq in test_ism.items():
        if z == 0:
            cubes_z_zero[x, y, z] = sq

    print('Testing cycle_map')
    if len(cubes_z_zero) != len(expected_layer_z_zero):
        print(f'\tWRONG!! len expected {len(expected_layer_z_zero)} but was {len(cubes_z_zero)}')
        return

    for n_coord, sq in cubes_z_zero.items():
        if n_coord not in expected_layer_z_zero:
            print(f'\tWRONG!! Found {n_coord} not expected')
            return

    print('\t\tRIGHT')


if __name__ == '__main__':
    with open('data/aoc2020-input-day17.txt', 'r') as f:
        sol_raw_map = [line.strip('\n') for line in f.readlines()]

    test_1 = ['.#.',
              '..#',
              '###']

    print('PART 1')
    # TEST PART 1
    ism = parse_map(test_1)
    foo = len(ism)
    print('Testing parse_map', 'RIGHT' if foo == 75 else f'WRONG!! Expected 75 but was {foo}')

    live_squares, ism = cycle_map(ism, 1, expand)

    expect_layer_z = {(0, 0, 0): False,
                      (0, 1, 0): False,
                      (0, 2, 0): False,
                      (1, 0, 0): True,
                      (1, 1, 0): False,
                      (1, 2, 0): True,
                      (2, 0, 0): False,
                      (2, 1, 0): True,
                      (2, 2, 0): True,
                      (-1, -1, 0): False,
                      (-1, 0, 0): False,
                      (-1, 1, 0): False,
                      (0, -1, 0): False,
                      (1, -1, 0): False,
                      (-1, 2, 0): False,
                      (-1, 3, 0): False,
                      (0, 3, 0): False,
                      (1, 3, 0): False,
                      (2, -1, 0): False,
                      (2, 3, 0): False,
                      (3, -1, 0): False,
                      (3, 0, 0): False,
                      (3, 1, 0): True,
                      (3, 2, 0): False,
                      (3, 3, 0): False,
                      (-2, -2, 0): False,
                      (-2, -1, 0): False,
                      (-2, 0, 0): False,
                      (-1, -2, 0): False,
                      (0, -2, 0): False,
                      (-2, 1, 0): False,
                      (-2, 2, 0): False,
                      (1, -2, 0): False,
                      (2, -2, 0): False,
                      (-2, 3, 0): False,
                      (-2, 4, 0): False,
                      (-1, 4, 0): False,
                      (0, 4, 0): False,
                      (1, 4, 0): False,
                      (2, 4, 0): False,
                      (3, -2, 0): False,
                      (3, 4, 0): False,
                      (4, -2, 0): False,
                      (4, -1, 0): False,
                      (4, 0, 0): False,
                      (4, 1, 0): False,
                      (4, 2, 0): False,
                      (4, 3, 0): False,
                      (4, 4, 0): False}

    test_cycle_map(ism, expect_layer_z)

    print('Testing count_active_squares (1)',
          'RIGHT' if live_squares == 11 else f'WRONG!! Expected 11 but was {live_squares}')

    live_squares, ism = cycle_map(ism, 1, expand)
    print('Testing count_active_squares (2)',
          'RIGHT' if live_squares == 21 else f'WRONG!! Expected 21 but was {live_squares}')

    live_squares, ism = cycle_map(ism, 1, expand)
    print('Testing count_active_squares (3)',
          'RIGHT' if live_squares == 38 else f'WRONG!! Expected 38 but was {live_squares}')

    live_squares, ism = cycle_map(ism, 1, expand)
    print('Testing count_active_squares (4)',
          'RIGHT' if live_squares == 58 else f'WRONG!! Expected 58 but was {live_squares}')

    live_squares, ism = cycle_map(ism, 1, expand)
    print('Testing count_active_squares (5)',
          'RIGHT' if live_squares == 101 else f'WRONG!! Expected 101 but was {live_squares}')

    live_squares, ism = cycle_map(ism, 1, expand)
    print('Testing count_active_squares (6)',
          'RIGHT' if live_squares == 112 else f'WRONG!! Expected 112 but was {live_squares}')

    # SOLUTION PART 1
    sol_int_map = parse_map(sol_raw_map)
    sol_part_1, _ = cycle_map(sol_int_map, 6, expand)

    print('SOLUTION PART 1:', sol_part_1)
    print()

    print('PART 2')
    # TEST PART 2
    ism = parse_map_v2(test_1)

    live_squares, ism = cycle_map(ism, 6, expand_v2)
    print('Testing count_active_squares (6)',
          'RIGHT' if live_squares == 848 else f'WRONG!! Expected 848 but was {live_squares}')

    # SOLUTION PART 2
    sol_int_map = parse_map_v2(sol_raw_map)
    sol_part_2, _ = cycle_map(sol_int_map, 6, expand_v2)

    print('SOLUTION PART 2:', sol_part_2)
