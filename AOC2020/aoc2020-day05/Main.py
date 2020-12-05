# DAY 5: Binary Boarding


# PART 1
def binary_search(search_instructions, lower_bound, upper_bound):
    """
    Performs a binary space partitioning search between lower_bound and upper_bound according with instructions
    stated in search_instructions.

    :param search_instructions: string of 'U' and/or 'D' to guide the search. U meaning take the upper zone, D meaning
        take the lower zone.
    :param lower_bound: Initial minimum value.
    :param upper_bound: Initial maximum value.
    :return: Lower bound when instructions are finished.
    """
    for step in search_instructions:
        middle = (upper_bound + lower_bound) // 2
        if step == 'U':
            lower_bound = middle + 1
        else:
            upper_bound = middle

    return lower_bound


def transform_symbols(instructions, lower_symbol, upper_symbol):
    """
    Changes all instances of lower_symbol by 'D' and upper_symbol by 'U' in instructions. This is made to be used in
    the binary partition search.

    :param instructions: string with symbols to convert.
    :param lower_symbol: Symbol representing to take the lower zone of the binary partition.
    :param upper_symbol: Symbol representing to take the upper zone.
    :return: string with the symbols replaced.
    """
    instructions = instructions.replace(upper_symbol, 'U')
    instructions = instructions.replace(lower_symbol, 'D')

    return instructions


def transform_instructions(instructions):
    """
    Takes a boarding pass, splits in row_instructions and col_instructions and replace symbols to the common symbols
    used by the binary partition search algorithm.

    :param instructions: a 10 symbol boarding pass.
    :return: two strings representing the instructions to get the row and column by the binary partition search.
    """
    row_instructions = instructions[:7]
    col_instructions = instructions[7:]

    row_instructions = transform_symbols(row_instructions, 'F', 'B')
    col_instructions = transform_symbols(col_instructions, 'L', 'R')

    return row_instructions, col_instructions


def get_coordinates_from_instructions(instructions):
    """
    Gets the row and column of  a boarding pass.

    :param instructions: A boarding pass.
    :return: The row and column of the boarding pass.
    """
    row_instructions, col_instructions = transform_instructions(instructions)
    row = binary_search(row_instructions, 0, 127)
    col = binary_search(col_instructions, 0, 7)

    return row, col


def get_seat_id(row, col):
    """
    Gets a seat ID given its row and column.

    :param row: Row of the seat.
    :param col: Column of the seat.
    :return: seat id.
    """
    return row * 8 + col


def get_seat_id_from(instructions):
    """
    Gets a seat id of a boarding pass.

    :param instructions: The boarding pass.
    :return: seat id
    """
    row, col = get_coordinates_from_instructions(instructions)
    return get_seat_id(row, col)


def test_function_part_1(fun, input_value, expected):
    result = fun(input_value)
    print('TESTING', fun, 'RIGHT' if result == expected else f'WRONG!! Expected {expected} but was {result}')


def get_max_id(boarding_passes):
    """
    Gets the maxium seat id of a list of boarding passes.

    :param boarding_passes: List of strings representing boarding passes.
    :return: Maximum seat id.
    """
    target_boarding_pass = None
    max_id = -1
    for boarding_pass in boarding_passes:
        pass_ID = get_seat_id_from(boarding_pass)
        if pass_ID > max_id:
            max_id = pass_ID
            target_boarding_pass = boarding_pass
    return target_boarding_pass, max_id


# PART 2
def get_our_seat(boarding_passes):
    """
    Given a set of continuous boarding passes finds a missing seat.

    :param boarding_passes: list of boarding passes.
    :return: Seat ID of a missing seat.
    """
    all_seats_id = [get_seat_id_from(boarding_pass) for boarding_pass in boarding_passes]
    all_seats_id.sort()
    for i in range(1, len(all_seats_id)):
        if all_seats_id[i] - all_seats_id[i-1] > 1:
            return all_seats_id[i-1] + 1


if __name__ == '__main__':
    # puzzle input
    with open('data/aoc2020-input-day05.txt', 'r') as f:
        boarding_passes = [boarding_pass.strip('\n') for boarding_pass in f.readlines()]

    print('PART 1')
    print('Testing instruction transformation')
    test_instructions = 'FBFBBFFRLR'
    new_row_instructions, new_col_instructions = transform_instructions(test_instructions)
    print('Row instruction',
          'RIGHT' if new_row_instructions == 'DUDUUDD' else f'WRONG! Expected DUDUUDD but was {new_row_instructions}')
    print('Col instruction',
          'RIGHT' if new_col_instructions == 'UDU' else f'WRONG! Expected UDU but was {new_row_instructions}')

    # TEST binary search
    print('Testing binary search')
    row_found = binary_search(new_row_instructions, 0, 127)
    col_found = binary_search(new_col_instructions, 0, 7)
    print('Row found', 'RIGHT' if row_found == 44 else f'WRONG!! Expected 44 but was {row_found}')
    print('Col found', 'RIGHT' if col_found == 5 else f'WRONG!! Expected 5 but was {row_found}')

    # TEST PART 1
    print('Test Part 1')
    test_function_part_1(get_seat_id_from, test_instructions, 357)
    test_function_part_1(get_seat_id_from, 'BFFFBBFRRR', 567)
    test_function_part_1(get_seat_id_from, 'FFFBBBFRRR', 119)
    test_function_part_1(get_seat_id_from, 'BBFFBBFRLL', 820)

    # TESTING get_max_ID
    max_ID = get_max_id([test_instructions, 'BFFFBBFRRR', 'FFFBBBFRRR', 'BBFFBBFRLL'])
    print('Test get_max_ID', 'RIGHT' if max_ID == 820 else f'WRONG! Expected 820 but was {max_ID}')

    # SOLVE PART 1
    sol_part_1 = get_max_id(boarding_passes)
    print('SOLUTION', sol_part_1)

    # PART 2
    print('PART 2')
    sol_part_2 = get_our_seat(boarding_passes)
    print('SOLUTION', sol_part_2)
