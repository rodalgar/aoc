# Day 9: Encoding Error


# PART 1
def parse_input(raw_input):
    """
    Parses a list of string representing int values to a list of int values.

    :param raw_input: List of string.
    :return: List of int.
    """
    return list(map(int, raw_input))


def get_values_two(values, target_sum):
    """
    Code from aoc2020 day 1. From the list 'values' picks two values whose sum is equal to target_sum.

    :param values: List of int values to chose from.
    :param target_sum: Value used for compare the sum of two elements of 'values'.
    :return: Tuple of (a, b, a+b, a*b) being 'a' and 'b' elements of 'values' or tuple (None, None, None, None) if a
        and b can't be found.
    """

    int_data = [int(x) for x in values]
    int_data.sort()

    for x in range(len(values)):
        for y in range(x+1, len(values)):
            suma = int_data[x] + int_data[y]
            if suma == target_sum:
                return int_data[x], int_data[y], suma, int_data[x] * int_data[y]
            elif suma > target_sum:
                break

    return None, None, None, None


def check_values(values, window_size, verbose=False):
    """
    Let window_size define a rolling window over 'values' of size 'window_size'. Let j be the immediate value following
    a window defined by window_size. This function uses a rolling window of size 'window_size' over 'values' and for
    each window tries to find two values inside it that sums exactly j. If, for any given window, two values can't be
    found, then j is incorrect and stored in a list to be returned.

    :param values: List of values to check.
    :param window_size: Size of window.
    :param verbose: If True more information will be printed.
    :return: List of j. Incorrect values.
    """

    bad_numbers = []
    i = 0
    j = window_size
    while j < len(values):
        window = values[i:j]
        target = values[j]
        if verbose:
            print('Checking window', window)
            print('Target is', target)
        one, two, three, _ = get_values_two(window, target)
        if one is None:
            if verbose:
                print(f'Target {target} Window {window} WRONG!!!')
            bad_numbers.append(target)
        i += 1
        j += 1

    return bad_numbers


# PART 2
def search_weakness(values, target, verbose=False):
    """
    Given a list of values and a target value, this function finds the first consecutive interval of values that sum
    exactly the target value. Then it fins the minimum and maximum values of that interval and returns their sum or
    None if no interval can be found.

    :param values: List of values to perform the search.
    :param target: Target value.
    :param verbose: If True more information will be printed.
    :return: If a consecutive interval of values that sums 'target' can be found, the sum of the minimum or maximum
    values is returned. None otherwise.
    """
    if verbose:
        print('Target is', target, 'in', values)
    for i in range(0, len(values)):
        if verbose:
            print('From', i)
        accum = values[i]
        minimum = values[i]
        maximum = values[i]
        j = i + 1
        processed_values = []
        while accum < target:
            if verbose:
                print('\tacum is', accum, '. Adding ', values[j])
            processed_values.append(values[j])
            accum += values[j]
            if values[j] < minimum:
                minimum = values[j]
            if values[j] > maximum:
                maximum = values[j]
            j += 1
        if accum == target:
            if verbose:
                print('FOUND!!', i, j, minimum, maximum, processed_values)
            return minimum + maximum
    return None


if __name__ == '__main__':
    with open('data/aoc2020-input-day09.txt', 'r') as f:
        sol_data = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    # TEST PART 1
    test_input = ['35',
                  '20',
                  '15',
                  '25',
                  '47',
                  '40',
                  '62',
                  '55',
                  '65',
                  '95',
                  '102',
                  '117',
                  '150',
                  '182',
                  '127',
                  '219',
                  '299',
                  '277',
                  '309',
                  '576']

    length_test_input = len(test_input)
    test_int_values = parse_input(test_input)
    print('Test parse_input',
          'RIGHT' if len(test_int_values) == length_test_input
          else f'WRONG!! Expected {length_test_input} but was {len(test_int_values)}')

    test_bads = check_values(test_int_values, 5)
    print('Test check_values, qty', 'RIGHT' if len(test_bads) == 1 else f'WRONG!! Expected 1 but was {len(test_bads)}')
    print('Test check_values, number',
          'RIGHT' if test_bads[0] == 127 else f'WRONG!! Expected 127 but was {test_bads[0]}')

    # SOLVE PART 1
    sol_bad_values = check_values(parse_input(sol_data), 25)
    sol_first_bad = sol_bad_values[0]
    print('SOLUTION PART 1', sol_first_bad)

    print('PART 2')
    test_weakness = search_weakness(test_int_values, 127)
    print('Test search_weakness', 'RIGHT' if test_weakness == 62 else f'WRONG!! Expected 62 but was {test_weakness}')

    # SOLVE PART 2
    sol_weakness = search_weakness(parse_input(sol_data), sol_first_bad)
    print('SOLUTION PART 2', sol_weakness)
