# Day 13: Shuttle Search


# PART 1
def parse_input(raw_input):
    """
    Parses a raw input into a minimum timestamp and a list of bus schedules.

    :param raw_input: String representing schedules of buses and a minimum timestamp.
    :return: Parsed input
    """
    if len(raw_input) != 2:
        raise Exception(f'Expected input with len 2, but was {len(raw_input)}')

    minimum_timestamp = int(raw_input[0])
    schedules = []
    for time in raw_input[1].split(','):
        if time == 'x':
            schedules.append(-1)
        else:
            schedules.append(int(time))
    return minimum_timestamp, schedules


def get_bus(minimum_timestamp, schedules):
    """
    Gets the best bus (the one which makes us wait the minimum, given a timestamp)

    :param minimum_timestamp: Moment in which we'll start waiting.
    :param schedules: Schedules of all buses.
    :return: Tuple of best bus and best waiting time.
    """
    waiting_times = []

    for time in schedules:
        if time > 0:
            waiting_times.append((time, ((minimum_timestamp // time) + 1) * time - minimum_timestamp))

    best_bus, best_waiting_time = waiting_times[0]
    for bus, wait in waiting_times[1:]:
        if wait < best_waiting_time:
            best_bus = bus
            best_waiting_time = wait

    return best_bus, best_waiting_time


# PART 2
def resolve_contest(schedules, verbose=False):
    """
    Given a list of schedules finds in which timestamp t all buses will be aligned, from t, as t+i being 'i' its column
    in the schedule.

    :param schedules: List of schedules.
    :param verbose: If True, additional info will be printed.
    :return: timestamp t of the alignment.
    """
    # Values of -1 represent buses without restrictions. That means that they can depart any minute. So we consider its
    # schedule as being 1 (each minute)
    curated_schedules = [1 if data == -1 else data for data in schedules]
    if verbose:
        print('\n\n')

    level_values = [0 for _ in curated_schedules]
    level_values[0] = curated_schedules[0]

    if verbose:
        print('schedules', schedules, 'level values', level_values)

    max_level = len(curated_schedules)
    num_iter = 0
    level = 1
    while level < max_level:
        if verbose:
            print(f'Level {level}')
        sch = curated_schedules[level]
        if verbose:
            print(f'Bus ID {sch}')

        last_value = level_values[level - 1] if level > 0 else 0
        value = level_values[level]

        if verbose:
            print(f'\tlevel_value {value} last level_value {last_value}')

        # We check if the actual level value is greater than its predecessor. If not we'll jump forward.
        level_difference = last_value - value
        if level_difference > 0:
            # We'll do ONLY one jump. We adjust jump length.
            jump_size = (level_difference // sch) + 1
            to_add = jump_size * sch
            # Jump!!
            value += to_add

        level_values[level] = value

        if level > 0:
            if verbose:
                print(f'Checking if {level_values[level]} - {level_values[level - 1]} == {1}')
        # At this point current level has a value greater than its predecessor. Now we have two possibilities... either
        # current value is EXACTLY 1 point greater than its predecessor (in that case they will be aligned) or not... in
        # that case all predecessor levels will need to jump. Level 0 is an special case as it has no predecessor.
        if level == 0 or (level_values[level] - level_values[level - 1] == 1):
            # Ok, we are good. Up until this level all is aligned, so we go on to the next!!
            if verbose:
                print('DING! Levels are aligned!!')
            level += 1
        else:
            if verbose:
                print(':( Levels are not aligned. Predecessor levels need to jump.')

            # Here we should calculate the Least Common Multiple of all the schedules of all predecessor levels.. BUT
            # a prior observation of values showed that all values are prime numbers, so the lcm of a list of prime
            # numbers is their product. This should be safely refactored into a function that calculates lcm. Someday...
            factor = 1
            for later_schedule in curated_schedules[0:level]:
                factor *= later_schedule
            if verbose:
                print(f'\tJump will be size {factor}')
                print(f'\tLevel values BEFORE the jump.', level, level_values)
            for i in range(level):
                if verbose:
                    print(f'\t\tLevel {i} is jumping!!')
                level_values[i] += factor
            if verbose:
                print(f'\tLevel values AFTER the jump.', level_values)

        if verbose:
            print('END OF ITERATION. OUTPUT OF ALL VARIABLES:')
            print(f'\tlevel', level)
            print(f'\tlevel_values', level_values)

        num_iter += 1
        # This overrides verbosity, but I find it interesting in big cases.
        if num_iter % 1000000 == 0:
            print(f'Iteration {num_iter}')
            print(f'\tlevel_values', level_values)

    if verbose:
        print(f'Problem solved in {num_iter} steps')

    return level_values[0], curated_schedules, level_values, num_iter


def test_part_2(schedules, expected):
    test_result, test_list, test_level_values, test_steps = resolve_contest(schedules)
    print('Test resolve_contest',
          f'RIGHT (Steps: {test_steps})' if test_result == expected
          else f'WRONG!! Expected {expected} but was {test_result}')


if __name__ == '__main__':
    with open('data/aoc2020-input-day13.txt', 'r') as f:
        sol_raw_notes = [line.strip('\n') for line in f.readlines()]

    test_raw_notes = ['939',
                      '7,13,x,x,59,x,31,19']

    print('PART 1')
    # TEST PART 1
    test_timestamp, test_schedules = parse_input(test_raw_notes)
    print('Test parse_input, timestamp',
          'RIGHT' if test_timestamp == 939 else f'WRONG!! Expected 939 but was {test_timestamp}')
    print('Test parse_input, schedules',
          'RIGHT' if test_schedules == [7, 13, -1, -1, 59, -1, 31, 19]
          else f"WRONG!! Expected [7,13,-1,-1,59,-1,31,19] but was {test_schedules}")

    test_best_bus, test_best_waiting_time = get_bus(test_timestamp, test_schedules)
    print('Test get_bus, bus', 'RIGHT' if test_best_bus == 59 else f'WRONG!! Expected 59 but was {test_best_bus}')
    print('Test get_bus, wait',
          'RIGHT' if test_best_waiting_time == 5 else f'WRONG!! Expected 5 but was {test_best_waiting_time}')

    # SOLVE PART 1
    sol_timestamp, sol_schedules = parse_input(sol_raw_notes)
    sol_best_bus, sol_best_waiting_time = get_bus(sol_timestamp, sol_schedules)
    print('SOLUTION PART 1:', sol_best_bus * sol_best_waiting_time)
    print()

    print('PART 2')
    # TEST PART 2
    test_part_2(test_schedules, 1068781)
    test_part_2([17, -1, 13, 19], 3417)
    test_part_2([67, 7, 59, 61], 754018)
    test_part_2([67, -1, 7, 59, 61], 779210)
    test_part_2([67, 7, -1, 59, 61], 1261476)
    test_part_2([1789, 37, 47, 1889], 1202161486)

    # SOLVE PART 2
    result, curated_list, all_level_values, steps = resolve_contest(sol_schedules)
    print(f'SOLUTION PART 2: {result} (steps {steps})')
