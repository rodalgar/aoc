# Day 12: Rain Risk
import re


# PART 1
def parse_instruction(instruction):
    """
    Parses an string instruction.

    :param instruction: Raw string instruction.
    :return: Tuple (x, y) as x = action and y an int value.
    """
    instruction_result = re.match("^([A-Z])(\d+)$", instruction)
    return instruction_result.group(1), int(instruction_result.group(2))


def parse_instructions(raw_instructions):
    """
    Parses a list of raw string instructions.

    :param raw_instructions: List of string representing a raw instruction.
    :return: List of tuple (x, y) as 'x' = action and 'y' an int value.
    """
    return list(map(parse_instruction, raw_instructions))


# Facing directions
DIR_NORTH = 0
DIR_EAST = 1
DIR_SOUTH = 2
DIR_WEST = 3


def move_to_direction(direction, value, actual_ew, actual_ns):
    """
    Returns modified coordinates given a direction and a value.

    :param direction: Facing direction.
    :param value: Units to move.
    :param actual_ew: Base value in the ew axis.
    :param actual_ns: Base value in the ns axis.
    :return:
    """
    if direction == DIR_NORTH:
        return actual_ew, actual_ns + value
    elif direction == DIR_EAST:
        return actual_ew + value, actual_ns
    elif direction == DIR_SOUTH:
        return actual_ew, actual_ns - value
    else:
        return actual_ew - value, actual_ns


def translate_direction(direction):
    """
    Transforms an string direction into its associated int value.

    :param direction: string direction.
    :return: associated int value from direction.
    """
    if direction == 'N':
        return DIR_NORTH
    elif direction == 'S':
        return DIR_SOUTH
    elif direction == 'E':
        return DIR_EAST
    elif direction == 'W':
        return DIR_WEST
    else:
        raise Exception(f'Unknown direction {direction}')


def navigate_p1(instructions):
    """
    Navigates the ship as per rules of part 1.

    :param instructions: List of parsed instructions.
    :return: tuple (x, y) as 'x' ew coordinate value and 'y' ns coordinate value.
    """

    ship_direction = DIR_EAST
    ns_axis = 0
    ew_axis = 0
    movement_commands = ['N', 'E', 'S', 'W']

    for action, value in instructions:
        if action in movement_commands:
            ew_axis, ns_axis = move_to_direction(translate_direction(action), value, ew_axis, ns_axis)
        elif action == 'R':
            spins = value / 90
            ship_direction = int((ship_direction + spins) % 4)
        elif action == 'L':
            spins = value / 90
            ship_direction = int((ship_direction - spins) % 4)
        elif action == 'F':
            ew_axis, ns_axis = move_to_direction(ship_direction, value, ew_axis, ns_axis)
        else:
            raise Exception(f'Unknown action {action} ({value})!')

    return ew_axis, ns_axis


def calculate_distance(ew_axis, ns_axis):
    """
    Calculates Manhattan distance fom (0, 0) to (ew_axis, ns_axis)

    :param ew_axis: value of ew axis.
    :param ns_axis: value of ns axis.
    :return:
    """
    return abs(ew_axis) + abs(ns_axis)


# PART 2
def navigate_p2(instructions):
    """
    Navigates the ship as per rules of part 2.

    :param instructions: List of parsed instructions.
    :return: tuple (x, y) as 'x' ew coordinate value and 'y' ns coordinate value.
    """

    # Ship coordinates
    ns_axis = 0
    ew_axis = 0
    # Way-point coordinates (relative to ship's)
    wp_ns_axis = 1
    wp_ew_axis = 10
    movement_commands = ['N', 'E', 'S', 'W']

    for action, value in instructions:
        if action in movement_commands:
            wp_ew_axis, wp_ns_axis = move_to_direction(translate_direction(action), value, wp_ew_axis, wp_ns_axis)
        elif action == 'F':
            ns_axis += value * wp_ns_axis
            ew_axis += value * wp_ew_axis
        elif action == 'R':
            # turning right rule: for each quadrant right: (x, y) => (y, -x)
            spins = int(value / 90)
            for s in range(spins):
                wp_ew_axis, wp_ns_axis = wp_ns_axis, -1 * wp_ew_axis
        elif action == 'L':
            # turning left rule: for each quadrant left: (x, y) => (-y, x)
            spins = int(value / 90)
            for s in range(spins):
                wp_ew_axis, wp_ns_axis = -1 * wp_ns_axis, wp_ew_axis

    return ew_axis, ns_axis


if __name__ == '__main__':
    with open('data/aoc2020-input-day12.txt', 'r') as f:
        sol_raw_instructions = [line.strip('\n') for line in f.readlines()]

    raw_test_instructions = ['F10',
                             'N3',
                             'F7',
                             'R90',
                             'F11']

    print('PART 1')
    # TEST PART 1
    expected_parsed_action = ('F', 10)
    result = parse_instruction('F10')
    print('Test parse_instruction, F10',
          'RIGHT' if result == expected_parsed_action
          else f'WRONG!! Expected {expected_parsed_action} but was {result}')
    expected_parsed_action = ('R', 90)
    result = parse_instruction('R90')
    print('Test parse_instruction, R90',
          'RIGHT' if result == expected_parsed_action
          else f'WRONG!! Expected {expected_parsed_action} but was {result}')

    test_instructions = parse_instructions(raw_test_instructions)
    ew, ns = navigate_p1(test_instructions)
    print('Test navigate_p1, ns', 'RIGHT' if ns == -8 else f'WRONG!! Expected -8 but was {ns}')
    print('Test navigate_p1, ew', 'RIGHT' if ew == 17 else f'WRONG!! Expected 17 but was {ew}')

    foo = calculate_distance(ew, ns)
    print('Test calculate_distance', 'RIGHT' if foo == 25 else f'WRONG!! Expected 25 but was {foo}')

    # SOLVE PART 1
    sol_instructions = parse_instructions(sol_raw_instructions)
    ew, ns = navigate_p1(sol_instructions)
    foo = calculate_distance(ew, ns)
    print('SOLUTION PART 1', foo)
    print()

    print('PART 2')
    # TEST PART 2
    ew, ns = navigate_p2(test_instructions)
    print('Test navigate_p2, ns', 'RIGHT' if ns == -72 else f'WRONG!! Expected -72 but was {ns}')
    print('Test navigate_p2, ew', 'RIGHT' if ew == 214 else f'WRONG!! Expected 214 but was {ew}')

    foo = calculate_distance(ew, ns)
    print('Test calculate_distance (2)', 'RIGHT' if foo == 286 else f'WRONG!! Expected 286 but was {foo}')

    # SOLVE PART 2
    ew, ns = navigate_p2(sol_instructions)
    foo = calculate_distance(ew, ns)
    print('SOLUTION  PART 2', foo)
