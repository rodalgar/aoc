# DAY 2


# Utility functions. Parsing, testing, solving.
def parse_password(raw_input):
    """
    Parses a raw input (in string form) to a tuple of values.

    :param raw_input: string in the form \d+-\d+ [a-z]+: [a-z]+
    :return: tuple (min, max, symbol, password) being:
        min: minimum number of occurrences of symbol.
        max: maximum number of occurrences of symbol.
        symbol: symbol under evaluation.
        password: password to check.
    """
    chunks = [chunk.strip() for chunk in raw_input.split(':')]
    condition = chunks[0]
    password = chunks[1]

    condition_chunks = condition.split(' ')
    symbol = condition_chunks[1]
    min_occurrences = int(condition_chunks[0].split('-')[0])
    max_occurrences = int(condition_chunks[0].split('-')[1])

    return min_occurrences, max_occurrences, symbol, password


def test_evaluation_method(evaluation_method, samples):
    """
    Runs the evaluation method over all samples and compare the evaluation method result with the expected value.

    :param evaluation_method: password evaluation function.
    :param samples: list of tuple of raw inputs and the expected result of the evaluation.
    :return: None.
    """
    for sample in samples:
        (values, expected) = sample
        password_tuple = parse_password(values)
        val = evaluation_method(password_tuple)

        print('Case', values, 'RIGHT' if val == expected else f'WRONG (was {val} but expected {expected})')


def solve_part(evaluation_method, samples):
    """
    Runs the evaluation method over all samples and counts every sample that passes the evaluation.

    :param evaluation_method: password evaluation function.
    :param samples: list parsed raw inputs.
    :return: number of samples that passes the evaluation.
    """
    counter = 0
    for sample in samples:
        val = evaluation_method(sample)
        if val:
            counter += 1
    return counter


# PART 1
def check_password_part1(password):
    (min_value, max_value, symbol, actual_password) = password

    occurrences = actual_password.count(symbol)

    return min_value <= occurrences <= max_value


# PART 2
def check_password_part2(password):
    (min_value, max_value, symbol, actual_password) = password

    occurrences = 0
    if actual_password[min_value-1] == symbol:
        occurrences += 1
    if actual_password[max_value-1] == symbol:
        occurrences += 1

    return occurrences == 1


if __name__ == '__main__':
    with open('data/aoc2020-input-day02.txt', 'r') as f:
        prod_samples = [parse_password(line.strip('\n')) for line in f.readlines()]

    # TEST PART 1
    test_samples_p1 = [('1-3 a: abcde', True), ('1-3 b: cdefg', False), ('2-9 c: ccccccccc', True)]
    test_evaluation_method(check_password_part1, test_samples_p1)
    # SOLVE PART 1
    print('SOLUTION', solve_part(check_password_part1, prod_samples))
    print()

    # TEST PART 2
    test_samples_p2 = [('1-3 a: abcde', True), ('1-3 b: cdefg', False), ('2-9 c: ccccccccc', False)]
    test_evaluation_method(check_password_part2, test_samples_p2)
    # SOLVE PART 2
    print('SOLUTION', solve_part(check_password_part2, prod_samples))
