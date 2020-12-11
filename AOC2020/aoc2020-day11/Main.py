# Day 11: Seating System
import numpy as np

# Constants representing state of a tile in the waiting area:
# There is no seat in the tile.
SEAT_NO_SEAT = 0
# There is an empty seat in the tile.
SEAT_EMPTY = 1
# There is an occupied seat in the tile.
SEAT_OCCUPIED = 2


# PART 1
def parse_room(raw_room):
    """
    Parses a string representing a waiting area into a numpy array with same size of input and with 3 possible values:
    1-0 if seat has no seat
    2-1 if seat is empty
    3-2 if seat is occupied

    :param raw_room: List of string representing a waiting area
    :return: numpy array os same shape of input.
    """
    height = len(raw_room)
    width = len(raw_room[0])

    # Initializing zero-matrix
    int_map = np.zeros([height, width], dtype=np.int)
    for num_line in range(height):
        line = raw_room[num_line]
        for num_col in range(width):
            symbol = line[num_col:num_col + 1]
            if symbol == 'L':
                int_map[num_line][num_col] = SEAT_EMPTY
            elif symbol == '#':
                int_map[num_line][num_col] = SEAT_OCCUPIED

    return int_map


def flatten_coordinates(height, width, max_width):
    """
    Flattens a 2-D coordinates into a 1-D value.
    :param height: y coordinate
    :param width: x coordinate
    :param max_width:  max width of waiting area.
    :return:
    """
    return (height * max_width) + width


def pre_calculate_adjacency_matrix_p1(waiting_area):
    """
    Iterates over every seat of the waiting area and obtain its adjacent seats as per part 1 rules:
    1-If seat is empty and there are no adjacent occupied seats, then the seat becomes occupied.
    2-If seat is occupied and there are 4+ adjacent occupied seats, then the seat becomes empty.

    :param waiting_area: A int 2D array representing a waiting area.
    :return: Dictionary with keys the flattened coordinates of the waiting area and a list of adjacent seats as values.
    """
    height = len(waiting_area)
    width = len(waiting_area[0])
    adjacent_seats = {}

    for h in range(height):
        for c in range(width):
            if waiting_area[h][c] == SEAT_NO_SEAT:
                continue
            position = flatten_coordinates(h, c, width)
            adjacent_seats[position] = []
            for i in range(h - 1, h + 2):
                for j in range(c - 1, c + 2):
                    if i == h and j == c:
                        continue
                    if (0 <= i < height) and (0 <= j < width):
                        # consider only adjacent if there is a seat
                        if waiting_area[i][j] != 0:
                            adjacent_seats[position].append((i, j))

    return adjacent_seats


def check_when_seat_empty(number_of_adjacent_seats):
    """
    Function to call when an empty seat is found when applying step.

    :param number_of_adjacent_seats: ditto.
    :return: True if problem condition is met, False otherwise.
    """
    return number_of_adjacent_seats == 0


def check_when_seat_occupied_p1(number_of_adjacent_seats):
    """
    Function to call when an occupied seat is found when applying step. It complies to rules set in part 1.

    :param number_of_adjacent_seats: ditto.
    :return: True if problem condition is met, False otherwise.
    """
    return number_of_adjacent_seats >= 4


def apply_step(waiting_area, adjacent_seats, check_when_occupied, check_when_empty):
    """
    Calculates one iteration of seat changes.

    :param waiting_area: numpy bi-dimensional array representing a waiting area.
    :param adjacent_seats: Dictionary of key (flattened coordinates of each seat) and value (list of coordinates of
    adjacent seats)
    :param check_when_occupied: function to apply when an occupied seat is found.
    :param check_when_empty: function to apply when an empty seat is found.
    :return: new numpy bi-dimensional array representing the new state of the waiting room, and whether the room has
    changed or not.
    """
    new_int_room = waiting_area.copy()
    is_modified = False

    height = len(waiting_area)
    width = len(waiting_area[0])

    for h in range(height):
        for c in range(width):
            value = waiting_area[h][c]
            if value == SEAT_NO_SEAT:
                continue
            # Calculating occupied adjacent seats
            seats_adjacent_to_seat = adjacent_seats[flatten_coordinates(h, c, width)]
            cnt_adjacent_seats = 0
            for adj_h, adj_c in seats_adjacent_to_seat:
                if waiting_area[adj_h][adj_c] == SEAT_OCCUPIED:
                    cnt_adjacent_seats += 1

            if value == SEAT_EMPTY:
                if check_when_empty(cnt_adjacent_seats):
                    new_int_room[h][c] = SEAT_OCCUPIED
                    is_modified = True
            elif value == SEAT_OCCUPIED:
                if check_when_occupied(cnt_adjacent_seats):
                    new_int_room[h][c] = SEAT_EMPTY
                    is_modified = True

    return new_int_room, is_modified


def populate_room(waiting_area, pre_calculate_adj, check_when_occupied, check_when_empty):
    """
    Calculate final state of waiting area by iterating until no change is obtained.

    :param waiting_area: numpy bi-dimensional array representing a waiting area.
    :param pre_calculate_adj: function used to obtain adjacent seats of each seat in the waiting area.
    :param check_when_occupied: function to apply when an occupied seat is found.
    :param check_when_empty: function to apply when an empty seat is found.
    :return: Final state of the waiting area and number of steps performed.
    """
    adjacent_seats = pre_calculate_adj(waiting_area)
    cnt_step = 0
    while True:
        new_int_room, has_changed = apply_step(waiting_area, adjacent_seats, check_when_occupied, check_when_empty)
        waiting_area = new_int_room
        if not has_changed:
            break
        cnt_step += 1

    return waiting_area, cnt_step


def count_total_seated(waiting_area):
    """
    Counts how many occupied seats are in a given waiting area.

    :param waiting_area: numpy bi-directional array representing a waiting area.
    :return: how many seats are occupied.
    """
    height = len(waiting_area)
    width = len(waiting_area[0])

    cnt_seated = 0
    for h in range(height):
        for c in range(width):
            value = waiting_area[h][c]
            if value == SEAT_OCCUPIED:
                cnt_seated += 1

    return cnt_seated


# PART 2
def pre_calculate_adjacency_matrix_p2(waiting_area):
    """
    Iterates over every seat of the waiting area and obtain its adjacent seats as per part 2 rules:
    1-If seat is empty and there are no adjacent occupied seats, then the seat becomes occupied.
    2-If seat is occupied and there are 5+ adjacent occupied seats, then the seat becomes empty.

    :param waiting_area: A int 2D array representing a waiting area.
    :return: Dictionary with keys the flattened coordinates of the waiting area and a list of adjacent seats as values.
    """

    height = len(waiting_area)
    width = len(waiting_area[0])
    adjacent_seats = {}
    # "Normalized" (i.e. modulus 1) direction vectors that will be used to expand the search from a central seat. There
    # is one for every direction around the seat. If one direction gets "out" of the waiting search or finds a seat then
    # that direction is removed from the active directions and it does not expand anymore. Expanding is done by
    # multiplying the "normalized" direction vectors by an step, beginning at 1, so every time we check all directions
    # and there are still directions (inside the waiting area) without a seat we try one step away from the initial
    # seat. This is done for every seat on the area.
    initial_directions = [(-1, -1), (-1, 0), (-1, 1),
                          (0, -1), (0, 1),
                          (1, -1), (1, 0), (1, 1)]
    for h in range(height):
        for c in range(width):
            # Only checks seats
            if waiting_area[h][c] == SEAT_NO_SEAT:
                continue
            position = flatten_coordinates(h, c, width)
            adjacent_seats[position] = []

            # For every seat we begin checking all directions, only one step away from the current seat.
            active_directions_to_check = initial_directions.copy()
            step = 1
            directions_to_stop_checking = []

            # We loop while there are still directions to check.
            while len(active_directions_to_check) > 0:
                for dy, dx in active_directions_to_check:
                    # Calculating adjacent tile coordinates to check if there is a seat or not.
                    y = (step * dy) + h
                    x = (step * dx) + c

                    # Checking if coordinates are inside the waiting area
                    if (y < 0) or (y >= height):
                        # Outside the waiting area. Don't check anything and mark direction as not active.
                        directions_to_stop_checking.append((dy, dx))
                        continue
                    # Checking if coordinates are inside the waiting area
                    if (x < 0) or (x >= width):
                        # Outside the waiting area. Don't check anything and mark direction as not active.
                        directions_to_stop_checking.append((dy, dx))
                        continue

                    # Tile is inside the waiting area, check if there is a seat.
                    if waiting_area[y][x] != 0:
                        # Ok, there is a seat. This is a valid adjacent tile. Keep coordinates and mark direction as
                        # not active.
                        adjacent_seats[position].append((y, x))
                        directions_to_stop_checking.append((dy, dx))

                # We just checked all active directions at this step. We generate a new set of "active" and increment
                # step size by 1.
                active_directions_to_check = [dire for dire in active_directions_to_check
                                              if dire not in directions_to_stop_checking]
                step += 1

    return adjacent_seats


def check_when_seat_occupied_p2(number_of_adjacent_seats):
    """
    Function to call when an occupied seat is found when applying step. It complies to rules set in part 2.

    :param number_of_adjacent_seats: ditto.
    :return: True if problem condition is met, False otherwise.
    """
    return number_of_adjacent_seats >= 5


if __name__ == '__main__':
    with open('data/aoc2020-input-day11.txt', 'r') as f:
        sol_room = [line.strip('\n') for line in f.readlines()]

    test_room = ['L.LL.LL.LL',
                 'LLLLLLL.LL',
                 'L.L.L..L..',
                 'LLLL.LL.LL',
                 'L.LL.LL.LL',
                 'L.LLLLL.LL',
                 '..L.L.....',
                 'LLLLLLLLLL',
                 'L.LLLLLL.L',
                 'L.LLLLL.LL']

    print('PART 1')
    expected_int_room = np.array([[1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
                                  [1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                                  [1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
                                  [1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
                                  [1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
                                  [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
                                  [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                  [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                                  [1, 0, 1, 1, 1, 1, 1, 0, 1, 1]])
    int_room = parse_room(test_room)
    print('Testing parse_room',
          'RIGHT' if np.equal(int_room, expected_int_room).all()
          else f'WRONG!! Expected {expected_int_room} but was {int_room}')

    adj = pre_calculate_adjacency_matrix_p1(int_room)
    expected_adj_seat_1_p1 = [(1, 0), (1, 1)]
    expected_adj_seat_1_p2 = None
    expected_adj_seat_1_p3 = [(0, 3), (1, 1), (1, 2), (1, 3)]
    print('Testing pre_calculate_adjacency_matrix_p1, 0_0',
          'RIGHT' if np.equal(expected_adj_seat_1_p1, adj[0]).all()
          else f'WRONG!! Expected {expected_adj_seat_1_p1} but was {adj[0]}')
    print('Testing pre_calculate_adjacency_matrix_p1, 0_1',
          'RIGHT' if 1 not in adj else f'WRONG!! Expected {False} but was {True}')
    print('Testing pre_calculate_adjacency_matrix_p1, 0_2',
          'RIGHT' if np.equal(expected_adj_seat_1_p3, adj[2]).all()
          else f'WRONG!! Expected {expected_adj_seat_1_p3} but was {adj[2]}')

    foo = check_when_seat_empty(0)
    print('Test check_when_seat_empty, 0', 'RIGHT' if foo else f'WRONG!! Expected True but was {foo}')
    foo = check_when_seat_empty(1)
    print('Test check_when_seat_empty, 1', 'RIGHT' if not foo else f'WRONG!! Expected False but was {foo}')

    foo = check_when_seat_occupied_p1(0)
    print('Test check_when_seat_occupied_p1, 0', 'RIGHT' if not foo else f'WRONG!! Expected False but was {foo}')
    foo = check_when_seat_occupied_p1(4)
    print('Test check_when_seat_occupied_p1, 4', 'RIGHT' if foo else f'WRONG!! Expected True but was {foo}')
    foo = check_when_seat_occupied_p1(5)
    print('Test check_when_seat_occupied_p1, 5', 'RIGHT' if foo else f'WRONG!! Expected True but was {foo}')

    expected_populated_room = np.array([[2, 0, 2, 1, 0, 1, 2, 0, 2, 2],
                                        [2, 1, 1, 1, 2, 1, 1, 0, 1, 2],
                                        [1, 0, 2, 0, 1, 0, 0, 2, 0, 0],
                                        [2, 1, 2, 2, 0, 2, 2, 0, 1, 2],
                                        [2, 0, 2, 1, 0, 1, 1, 0, 1, 1],
                                        [2, 0, 2, 1, 2, 1, 2, 0, 2, 2],
                                        [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                        [2, 1, 2, 1, 2, 2, 1, 2, 1, 2],
                                        [2, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                                        [2, 0, 2, 1, 2, 1, 2, 0, 2, 2]])

    test_populated, test_steps = populate_room(int_room, pre_calculate_adjacency_matrix_p1, check_when_seat_occupied_p1,
                                               check_when_seat_empty)
    print('Testing populate_room, last state',
          'RIGHT' if np.equal(expected_populated_room, test_populated).all()
          else f'WRONG!! Expected {expected_populated_room} but was {test_populated}')
    print('Testing populate_room, steps',
          'RIGHT' if test_steps == 5 else f'WRONG!! Expected 5 but was {test_steps}')

    cnt = count_total_seated(test_populated)
    print('Test count_total_seated', 'RIGHT' if cnt == 37 else f'WRONG!! Expected 37 but was {cnt}')

    # SOLVING PART 1
    sol_int_room = parse_room(sol_room)
    sol_populated, sol_steps = populate_room(sol_int_room, pre_calculate_adjacency_matrix_p1,
                                             check_when_empty=check_when_seat_empty,
                                             check_when_occupied=check_when_seat_occupied_p1)
    sol_cnt = count_total_seated(sol_populated)
    print('SOLUTION PART 1', sol_cnt)

    print('PART 2')
    adj_p2 = pre_calculate_adjacency_matrix_p2(int_room)
    expected_adj_seat_2_p1 = [(1, 0), (1, 1), (0, 2)]
    expected_adj_seat_2_p2 = None
    expected_adj_seat_2_p3 = [(0, 3), (1, 1), (1, 2), (1, 3), (0, 0)]
    print('Testing pre_calculate_adjacency_matrix_p2, 0_0',
          'RIGHT' if np.equal(expected_adj_seat_2_p1, adj_p2[0]).all()
          else f'WRONG!! Expected {expected_adj_seat_2_p1} but was {adj_p2[0]}')
    print('Testing pre_calculate_adjacency_matrix_p2, 0_1',
          'RIGHT' if 1 not in adj_p2 else f'WRONG!! Expected {False} but was {True}')
    print('Testing pre_calculate_adjacency_matrix_p2, 0_2',
          'RIGHT' if np.equal(expected_adj_seat_2_p3, adj_p2[2]).all()
          else f'WRONG!! Expected {expected_adj_seat_2_p3} but was {adj_p2[2]}')

    foo = check_when_seat_occupied_p2(0)
    print('Test check_when_seat_occupied_p2, 0', 'RIGHT' if not foo else f'WRONG!! Expected False but was {foo}')
    foo = check_when_seat_occupied_p2(4)
    print('Test check_when_seat_occupied_p2, 4', 'RIGHT' if not foo else f'WRONG!! Expected False but was {foo}')
    foo = check_when_seat_occupied_p2(5)
    print('Test check_when_seat_occupied_p2, 5', 'RIGHT' if foo else f'WRONG!! Expected True but was {foo}')

    test_populated, test_steps = populate_room(int_room, pre_calculate_adjacency_matrix_p2, check_when_seat_occupied_p2,
                                               check_when_seat_empty)

    expected_populated_room = [[2, 0, 1, 2, 0, 1, 2, 0, 1, 2],
                               [2, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                               [1, 0, 1, 0, 1, 0, 0, 2, 0, 0],
                               [2, 2, 1, 2, 0, 2, 1, 0, 1, 2],
                               [1, 0, 1, 2, 0, 1, 1, 0, 1, 2],
                               [2, 0, 1, 1, 1, 1, 2, 0, 1, 1],
                               [0, 0, 2, 0, 1, 0, 0, 0, 0, 0],
                               [1, 1, 1, 2, 2, 2, 1, 1, 1, 2],
                               [2, 0, 1, 1, 1, 1, 1, 2, 0, 1],
                               [2, 0, 1, 2, 1, 1, 2, 0, 1, 2]]

    print('Testing populate_room (p2), last state',
          'RIGHT' if np.equal(expected_populated_room, test_populated).all()
          else f'WRONG!! Expected {expected_populated_room} but was {test_populated}')
    print('Testing populate_room (p2), steps',
          'RIGHT' if test_steps == 6 else f'WRONG!! Expected 6 but was {test_steps}')

    cnt = count_total_seated(test_populated)
    print('Test count_total_seated (p2)', 'RIGHT' if cnt == 26 else f'WRONG!! Expected 26 but was {cnt}')

    # SOLVING PART 2
    sol_populated, sol_steps = populate_room(sol_int_room, pre_calculate_adjacency_matrix_p2,
                                             check_when_empty=check_when_seat_empty,
                                             check_when_occupied=check_when_seat_occupied_p2)
    sol_cnt = count_total_seated(sol_populated)
    print('SOLUTION PART 2', sol_cnt)
