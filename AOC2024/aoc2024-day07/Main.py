# Day 7: Bridge Repair
import operator
from collections import namedtuple

test_raw_data = [
    '190: 10 19',
    '3267: 81 40 27',
    '83: 17 5',
    '156: 15 6',
    '7290: 6 8 6 15',
    '161011: 16 10 13',
    '192: 17 8 14',
    '21037: 9 7 18 13',
    '292: 11 6 16 20'
]

Operation = namedtuple('Operation', 'test_value numbers')


def parse_input(raw_data: [str]) -> [Operation]:
    operations = []
    for line in raw_data:
        test_value, str_numbers = line.split(':')
        numbers = list(map(int, str_numbers.strip(' ').split(' ')))
        operations.append(Operation(int(test_value), numbers))

    return operations


test_operations = parse_input(test_raw_data)
print(test_operations)


def concat_numbers(a: int, b: int) -> int:
    exp = 10 ** len(str(b))
    return a * exp + b


def check_operation(operation: Operation, operators, verbose: bool = False) -> bool:
    head_combinations = [(operation.numbers[0], 1)]

    while len(head_combinations) > 0:
        combination = head_combinations[0]
        head_combinations = head_combinations[1:]

        accrued_value, ix_number = combination

        for op in operators:
            next_number = operation.numbers[ix_number]
            next_value = op(accrued_value, next_number)

            # As all operations increase accrued value, if it gets bigger than the test value then this combination
            # is wrong.
            if next_value > operation.test_value:
                continue

            # if this is the last number of the combination we check with test value.
            if ix_number == len(operation.numbers) - 1:
                if next_value == operation.test_value:
                    # It's possible that several combinations get the same test value
                    # However, we only need one (so far) so, we don't need any more computations
                    return True
            else:
                # New combination
                head_combinations.append((next_value, ix_number + 1))

    # reaching this point means that no combination gets you the test value.
    return False


def part1(all_operations: [Operation]) -> int:
    operators = [operator.mul, operator.add]
    return sum([operation.test_value for operation in all_operations if check_operation(operation, operators)])


def part2(all_operations: [Operation]) -> int:
    operators = [operator.mul, operator.add]
    first_evaluation = [(check_operation(operation, operators), operation) for operation in all_operations]

    first_evaluation_value = sum([operation.test_value for result, operation in first_evaluation if result])
    wrong_first_evaluation = [operation for result, operation in first_evaluation if not result]

    operators = [concat_numbers, operator.mul, operator.add]
    second_evaluation_value = sum([operation.test_value for operation in wrong_first_evaluation
                                   if check_operation(operation, operators)])

    return first_evaluation_value + second_evaluation_value


if __name__ == '__main__':
    with open('data/aoc2024-input-day07.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_operations = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', part1(sol_operations))

    print('PART 2')
    print('>>>>SOLUTION: ', part2(sol_operations))
