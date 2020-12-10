# Day 10: Adapter Array


# PART 1
def parse_input(raw_input):
    """
    Parses a list of string representing int values to a list of int values.

    :param raw_input: List of string.
    :return: List of int.
    """
    return list(map(int, raw_input))


def sequence_jolts(adapters):
    """
    This function receive a list of int, sorts it and calculate distance between every element and the next.

    :param adapters: List of int representing joltage of adapters.
    :return: Dictionary formed for how many times (values) each difference between adapters occurs (keys)
    """
    the_adapters = adapters[:]
    # Adding the device's built in joltage adapter
    the_adapters.append(max(the_adapters) + 3)
    the_adapters.sort()

    # Initializing to charging outlet
    last_adapter = 0
    differences = {1: 0,
                   2: 0,
                   3: 0}
    for ad in the_adapters:
        differences[ad - last_adapter] += 1
        last_adapter = ad

    return differences


# PART 2
def get_adapter_combinations(adapters, verbose=False):
    """
    Obtains how many different valid combinations of connections between a list of adapters.

    We sort adapters by joltage in ascending order, and begin from the last one (device adapter) noting how many
    adapters can be connected with it, and save the number on a dictionary by the connector joltage. Then we loop from
    last adapter to first one summing this value for every adapter which can be connected and save it under adapter
    joltage.
    So each adapter has a value that is the sum of the values of all directly reachable adapters.

    :param adapters: List of adapters.
    :param verbose: If True additional information will be printed.
    :return: Number of valid combinations.
    """
    the_adapters = adapters[:]
    the_adapters.append(0)
    handheld_adapter = max(the_adapters) + 3
    the_adapters.append(handheld_adapter)
    the_adapters.sort()
    if verbose:
        print(the_adapters)
    combinations_from_adapter = {handheld_adapter: 1}

    for j in range(len(the_adapters) - 2, -1, -1):
        adapter = the_adapters[j]
        if verbose:
            print(adapter)
        cnt = 0
        for i in range(1, 4):
            next_adapter = adapter + i
            if verbose:
                print(f'\t{next_adapter}')
            if next_adapter in the_adapters:
                if verbose:
                    print('\t\t\tOK!!')
                cnt += combinations_from_adapter[next_adapter]
        if verbose:
            print(f'From adapter {adapter} are {cnt} combinations')
        combinations_from_adapter[adapter] = cnt

    return cnt


if __name__ == '__main__':
    with open('data/aoc2020-input-day10.txt', 'r') as f:
        sol_raw = [line.strip('\n') for line in f.readlines()]

    test_small = ['16',
                  '10',
                  '15',
                  '5',
                  '1',
                  '11',
                  '7',
                  '19',
                  '6',
                  '12',
                  '4']

    test_large = ['28',
                  '33',
                  '18',
                  '42',
                  '31',
                  '14',
                  '46',
                  '20',
                  '48',
                  '47',
                  '24',
                  '23',
                  '49',
                  '45',
                  '19',
                  '38',
                  '39',
                  '11',
                  '1',
                  '32',
                  '25',
                  '35',
                  '8',
                  '17',
                  '7',
                  '9',
                  '4',
                  '2',
                  '34',
                  '10',
                  '3']

    # PART 1
    print('PART 1')
    small = parse_input(test_small)
    print('Testing parse_input', 'RIGHT' if len(small) == 11 else f'WRONG!! Expected 11 but was {len(small)}')

    gro = sequence_jolts(small)
    print('Testing sequence_jolts, small, length 1', 'RIGHT' if gro[1] == 7 else f'WRONG!! Expected 7 but was {gro[1]}')
    print('Testing sequence_jolts, small, length 2', 'RIGHT' if gro[2] == 0 else f'WRONG!! Expected 0 but was {gro[2]}')
    print('Testing sequence_jolts, small, length 3', 'RIGHT' if gro[3] == 5 else f'WRONG!! Expected 5 but was {gro[3]}')

    large = parse_input(test_large)
    gro = sequence_jolts(large)
    print('Testing sequence_jolts, large, length 1',
          'RIGHT' if gro[1] == 22 else f'WRONG!! Expected 22 but was {gro[1]}')
    print('Testing sequence_jolts, large, length 2',
          'RIGHT' if gro[2] == 0 else f'WRONG!! Expected 0 but was {gro[2]}')
    print('Testing sequence_jolts, large, length 3',
          'RIGHT' if gro[3] == 10 else f'WRONG!! Expected 10 but was {gro[3]}')

    sol_adapters = parse_input(sol_raw)
    sol_diffs = sequence_jolts(sol_adapters)
    print('SOLUTION PART 1', sol_diffs[1] * sol_diffs[3])
    print()

    # PART 2
    print('PART 2')
    foo = get_adapter_combinations(small)
    print('Testing get_adapter_combinations, small',
          'RIGHT' if foo == 8 else f'WRONG!! Expected 8 but was {foo}')
    foo = get_adapter_combinations(large)
    print('Testing get_adapter_combinations, large',
          'RIGHT' if foo == 19208 else f'WRONG!! Expected 19208 but was {foo}')

    # SOLUTION
    foo = get_adapter_combinations(sol_adapters)
    print('SOLUTION PART 2', foo)
