# Day 23: Crab Cups
import cProfile


def parse_raw_labeling(raw_labeling):
    """
    Parses input string into a list of integer.
    :param raw_labeling: String representing an array of integer.
    :return: list of integer
    """

    return [int(i) for i in raw_labeling]


def pick_up_cups(cups, window_size, active_index, verbose=False):
    """
    Given a list of int and an starting position (active_index) picks up the 'window_size' elements immediate to the
    element at starting position. If 'position' and 'window_size' overflows the list of cups, it cycles from the
    beginning.

    :param cups: List of integer from which pick up the items.
    :param window_size: How many consecutive elements to pick pu.
    :param active_index: Position from where to pick pu elements.
    :param verbose: If True additional info will be printed.
    :return: List of size 'window_size' elements.
    """
    max_len = len(cups)

    if verbose:
        print(f'\tactive_index {active_index} + window_size {window_size} >= max_len {max_len} ?')
    if active_index + window_size >= max_len:
        pivot = active_index + window_size - max_len
        if verbose:
            print(f'\t\tpivot {pivot}')
        pick_up = cups[active_index + 1:]
        pick_up = pick_up + cups[:pivot + 1]
    else:
        pick_up = cups[active_index + 1:active_index + 1 + window_size]

    return pick_up


def do_move(cups, number_of_moves=1, verbose=False):
    """
    Performs 'number_of_moves' steps of the cups game.
    :param cups: List of integer representing the labels of the cups.
    :param number_of_moves: Number of moves to perform.
    :param verbose: If True additional info will be printed.
    :return: Final state of the cups list after 'number_of_moves' movements.
    """
    # select active cup
    max_cup_value = max(cups)
    if verbose:
        print(f'max label of cups: {max_cup_value}')
    active_cup_index = 0
    active_cup_label = cups[active_cup_index]
    actual_movement = 0
    while actual_movement < number_of_moves:
        if verbose:
            print(f'-- Move {actual_movement + 1} --')
            print(cups)
        # pick up 3
        # pick_up = cups[active_cup_index + 1:active_cup_index + 4]
        pick_up = pick_up_cups(cups, 3, active_cup_index, verbose)
        # cups = cups[0:active_cup_index + 1] + cups[active_cup_index + 4:]
        for item in pick_up:
            cups.remove(item)
        if verbose:
            print(f'this is the 3 picked up: {pick_up}')
            print(f'this is how the cups look without the picked up {cups}')
        # select destination
        destination_value = active_cup_label - 1
        if destination_value == 0:
            destination_value = max_cup_value
        # if destination_value in pick_up:
        #     print(f'destination should be {destination_value} but is in pick_up: {pick_up}')
        while destination_value in pick_up:
            if verbose:
                print(f'destination should be {destination_value} but is in pick_up: {pick_up}.')
            destination_value = destination_value - 1
            if destination_value == 0:
                destination_value = max_cup_value
        if verbose:
            print(f'destination value: {destination_value}')
        # place cups
        destination_idx = cups.index(destination_value)
        if verbose:
            print(f'destination value of {destination_value} found at index {destination_idx}')
        cups = cups[0:destination_idx + 1] + pick_up + cups[destination_idx + 1:]
        if verbose:
            print(f'cups after placement: {cups}')
        # select new active cup
        # active_cup_index = (active_cup_index + 1) % len(cups)
        active_cup_index = (cups.index(active_cup_label) + 1) % max_cup_value
        active_cup_label = cups[active_cup_index]
        if verbose:
            print(f'new active cup index is {active_cup_index} (cup label {cups[active_cup_index]})')
        # loop control
        actual_movement += 1
        if actual_movement % 1000 == 0:
            print(f'actual movement {actual_movement}')
        if verbose:
            print(20 * '-')

    return cups


def solve_part_1(cups):
    """
    Solves part 1 by transforming a list representing cup labels and returns labels following label '1'

    :param cups: List of cup labels.
    :return: String with labels of cups following '1'.
    """
    # obtain sequence from '1'
    index_one = cups.index(1)
    final_sequence = pick_up_cups(cups, 8, index_one)
    final_sequence = ''.join(map(str, final_sequence))

    return final_sequence


# PART 2
def expand_cups(cups, max_label, verbose=False):
    """
    Expands a list of cup labels adding values until 'max_label'.

    :param cups: Original list of cups.
    :param max_label: Maximum returned value.
    :param verbose: If True additional info will be printed.
    :return: Expanded list of cup labels.
    """
    max_used = max(cups)
    remaining = list(range(max_used + 1, max_label + 1))

    if verbose:
        print(f'cups {cups}')
        print(f'min cups {min(cups)}')
        print(f'max cups {max(cups)}')
        print(f'min ex cups {min(remaining)}')
        print(f'max ex cups {max(remaining)}')

    return cups + remaining


if __name__ == '__main__':
    sol_raw_cups = '253149867'
    test_raw_cups = '389125467'

    print('PART 1')
    # TEST PART 1
    expected_parsed_cups = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    test_cups = parse_raw_labeling(test_raw_cups)
    print('Testing parse_raw_labeling',
          'RIGHT' if expected_parsed_cups == test_cups
          else f'WRONG!! Expected {expected_parsed_cups} but was {test_cups}')

    expected_picked_up_cups = [3, 4, 5, 6]
    test_picked_up_cups = pick_up_cups([1, 2, 3, 4, 5, 6, 7, 8], 4, 1)
    print('Testing pick_up_cups, inside',
          'RIGHT' if expected_picked_up_cups == test_picked_up_cups
          else f'WRONG!! Expected {expected_picked_up_cups} but was {test_picked_up_cups}')

    expected_picked_up_cups = [7, 8, 1, 2]
    test_picked_up_cups = pick_up_cups([1, 2, 3, 4, 5, 6, 7, 8], 4, 5)
    print('Testing pick_up_cups, cycle',
          'RIGHT' if expected_picked_up_cups == test_picked_up_cups
          else f'WRONG!! Expected {expected_picked_up_cups} but was {test_picked_up_cups}')

    expected_moved_cups = [2, 9, 1, 6, 7, 3, 8, 4, 5]
    test_final_cups = do_move(test_cups, 100)
    print('Testing do_move, 100',
          'RIGHT' if expected_moved_cups == test_final_cups
          else f'WRONG!! Expected {expected_moved_cups} but was {test_final_cups}')

    expected_final_sequence_10 = '92658374'
    test_final_seq = solve_part_1([5, 8, 3, 7, 4, 1, 9, 2, 6])
    print('Testing solve_part_1, 10',
          'RIGHT' if expected_final_sequence_10 == test_final_seq
          else f'WRONG!! Expected {expected_final_sequence_10} but was {test_final_seq}')

    expected_final_sequence_100 = '67384529'
    test_final_seq = solve_part_1(test_final_cups)
    print('Testing solve_part_1, 100',
          'RIGHT' if expected_final_sequence_100 == test_final_seq
          else f'WRONG!! Expected {expected_final_sequence_100} but was {test_final_seq}')

    # SOLVE PART 1
    sol_cups = parse_raw_labeling(sol_raw_cups)
    sol_final_cups = do_move(sol_cups, 100)
    print('PART 1 SOLUTION:', solve_part_1(sol_final_cups))
    print()

    print('PART 2')
    print('PART 2 is still work in progress!')
    quit()

    # TEST PART 2
    # sol_expanded_cups = expand_cups(sol_final_cups, 1000000)
    # sol_fdo_move(sol_expanded_cups, 10000000)

    max_cups_p2 = 1000000
    turns_p2 = 10000

    test_expanded_cups = expand_cups(test_final_cups, max_cups_p2, verbose=True)

    pr = cProfile.Profile()
    pr.enable()
    test_final_cups_p2 = do_move(test_expanded_cups, turns_p2)
    pr.disable()
    pr.print_stats(sort="cumtime")

    # SOLVE PART 2
