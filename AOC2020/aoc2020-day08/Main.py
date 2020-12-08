# DAY 8: Handheld Halting
import re

# PART 1
# COMMANDS, nop, jmp and acc
COMMAND_NOP = 0
COMMAND_JMP = 1
COMMAND_ACC = 2

# RESULTS
# If goes well
RESULT_OK = 0
# If an unknown command is found
RESULT_UNKNOWN_COMMAND = 1
# If instruction pointer falls outside the program
RESULT_IP_OUT_OF_BOUNDS = 2
# If an infinite loop is detected (trying to execute an already visited instruction)
RESULT_INFINITE_LOOP_DETECTED = 3


def get_command(raw_command):
    """
    Translates a raw input command into a revised command. Filters unexpected commands.

    :param raw_command: Command to parse.
    :return: int constant with a sanitized command.
    """
    if raw_command == 'nop':
        return COMMAND_NOP
    elif raw_command == 'jmp':
        return COMMAND_JMP
    elif raw_command == 'acc':
        return COMMAND_ACC
    else:
        raise Exception(f'Unknown command {raw_command}')


def get_number(raw_number):
    """
    Parses int number.

    :param raw_number: Number to parse.
    :return: int parsed number.
    """
    try:
        return int(raw_number)
    except TypeError as e:
        print(f"Raw number was {raw_number}. Can't be converted to int!!")


def parse_program(raw_program):
    """
    Transforms a list of string representing a program into a list of (x, y) tuple being x a sanitized command and
    y the int value.

    :param raw_program: List of strings representing a program.
    :return: Parsed program.
    """

    tokens = []
    for line in raw_program:
        chunks = line.split(' ')
        command = get_command(chunks[0])
        number = get_number(chunks[1])
        tokens.append((command, number))

    return tokens


def run_program_from_state(program, acc, ip, visited, verbose=False):
    """
    Runs a program beginning from a given state (accumulator, instruction pointer and visited instructions)

    :param verbose: If True additional info will be printed.
    :param program: Program to run.
    :param acc: Initial state of accumulator.
    :param ip: Initial state of the instruction pointer.
    :param visited: Initial state of de visited_position set.
    :return: Tuple of state and accumulator.
    """
    accumulator = acc
    instruction_pointer = ip
    visited_position = set(visited)
    last_instruction = len(program)

    while instruction_pointer != last_instruction:
        if verbose:
            print(f'IP {instruction_pointer} acc {accumulator} visited {visited_position}')
        if instruction_pointer in visited_position:
            return RESULT_INFINITE_LOOP_DETECTED, accumulator
        visited_position.add(instruction_pointer)
        if (instruction_pointer < 0) or (instruction_pointer >= len(program)):
            if verbose:
                print('instruction pointer is', instruction_pointer, len(program))
            return RESULT_IP_OUT_OF_BOUNDS, accumulator
        (command, number) = program[instruction_pointer]
        if command == COMMAND_ACC:
            accumulator += number
            instruction_pointer += 1
        elif command == COMMAND_JMP:
            instruction_pointer += number
        elif command == COMMAND_NOP:
            instruction_pointer += 1
        else:
            if verbose:
                print('Unknown command', command)
            return RESULT_UNKNOWN_COMMAND, accumulator

    return RESULT_OK, accumulator


def run_program(program):
    """
    Runs a program from the beginning ie, accumulator = 0 and instruction_pointer = 0

    :param program: program to run
    :return: Tuple of state and accumulator
    """
    return run_program_from_state(program, 0, 0, set())


# PART 2
def check_proposed_change(number, command, new_instruction, visited_position, max_pos):
    """
    Checks if changing from nop to jmp, or jmp to nop seems a good change. This is used to avoid wasting time doing
    changes that are not going to end well in cases when it is very clear.

    :param number: value given with command.
    :param new_instruction: new intruction poiner when change is accepted.
    :param visited_position: set of already visited instructions to check for infinite loops.
    :param max_pos: max size of program, to check if new instruction pointer is in bounds.
    :return: True if it seems a good change, False otherwise.
    """

    good_change = False
    if command == COMMAND_NOP and number == 0:
        print('\t\tNumber is 0, jmp 0 would lead to infinite loop.')
    elif new_instruction in visited_position:
        print(f'\t\tChange would lead to instruction {new_instruction} that has been already visited.')
    elif new_instruction < 0 or new_instruction > max_pos:
        print(f'\t\tChange would lead to instruction {new_instruction} that is out of bounds.')
    else:
        good_change = True

    return good_change


def probe_change_in_program(program, proposed_change, instruction_pointer, accumulator, visited_position):
    """
    Performs a copy of the program in which proposed_change is applied. Then it runs the modified program with the
    real values of accumulator, instruction pointer and visited positions and returns whether execution ended OK.

    :param program: program to modify and run.
    :param proposed_change: proposed modification.
    :param instruction_pointer: actual instruction pointer.
    :param accumulator: actual value of accumulator.
    :param visited_position: set of instructions already visited.
    :return: Whether modified program was correctly executed or not (and resulting accumulator)
    """
    changed_program = program[:]
    changed_program[instruction_pointer] = proposed_change

    new_status, new_acc = run_program_from_state(changed_program, accumulator, instruction_pointer,
                                                 visited_position)

    return new_status == RESULT_OK, new_acc


def repair_program(program, verbose=False):
    """
    We run the program instruction by instruction, until a potential change can be made. We check if change is any good,
    considering:
        1- Any nop can be changed to jmp unless jump destination has been already visited (it needs to be refined
        because what makes this a bad decision is to find a reachable visited instruction not necessarily the first
        one, but o well.) because that leads to an infinite loop.
        2- Changing nop +0 to jmp +0 leads to an infinite loop.
        3- Changing jmp x to nop x is valid unless the next instruction has been already visited (also, needs to be
        refined like case 1)
        4- Changing nop x to jmp x could lead to an instruction outside the program.
    As the program is corrupted, we know that some intervention needs to be done, so we'll try every chance to make a
    change and see what happens. We also know that we need to make ONLY ONE change, so there will not be ramifications
    after the first modification
    Every time we make a change, we run the modified program from that point and see the exit result. If it ends well
    we also know the final value of the accumulator so we can return it. If it does not end well, we ignore the change
    and continue executing the main program until the next chance arises or the program ends.

    :param verbose: If True additional info will be printed.
    :param program: the program to repair.
    :return: final value of accumulator.
    """

    accumulator = 0
    instruction_pointer = 0
    visited_position = set()

    while instruction_pointer not in visited_position:
        if verbose:
            print(f'M IP {instruction_pointer} acc {accumulator}')
        assert 0 <= instruction_pointer < len(program), \
            f'Instruction pointer is out of bounds!! Was {instruction_pointer} max {len(program)}'

        (command, number) = program[instruction_pointer]
        if verbose:
            print('Instruction', instruction_pointer, 'considering', command, number)
        if command == COMMAND_NOP:
            # nop is a change candidate. Check if change is safe.
            if verbose:
                print(f'\tConsidering change nop {number} to jmp {number}')
            new_instruction = instruction_pointer + number
            if check_proposed_change(number, command, new_instruction, visited_position, len(program)):
                was_good, new_acc = probe_change_in_program(program, (COMMAND_JMP, number), instruction_pointer,
                                                            accumulator, visited_position)
                if was_good:
                    if verbose:
                        print('Change was OK!')
                    return new_acc

        elif command == COMMAND_JMP:
            # jmp is a change candidate. Check if change is safe.
            if verbose:
                print(f'\tConsidering change jmp {number} to nop {number}')
            new_instruction = instruction_pointer + 1
            if check_proposed_change(number, command, new_instruction, visited_position, len(program)):
                # change looks good, let's try
                was_good, new_acc = probe_change_in_program(program, (COMMAND_NOP, number), instruction_pointer,
                                                            accumulator, visited_position)
                if was_good:
                    if verbose:
                        print('Change was OK!')
                    return new_acc

        # In this point either command was ACC or it was NOP/JMP and the change was illegal or not good. That's OK,
        # we execute the command.
        visited_position.add(instruction_pointer)

        if command == COMMAND_ACC:
            accumulator += number
            instruction_pointer += 1
        elif command == COMMAND_JMP:
            instruction_pointer += number
        elif command == COMMAND_NOP:
            instruction_pointer += 1
        else:
            raise Exception(f'Unknown command {command}!!')
    return accumulator


if __name__ == '__main__':
    with open('data/aoc2020-input-day08.txt', 'r') as f:
        sol_raw_program = [line.strip('\n') for line in f.readlines()]

    test_input = ['nop +0',
                  'acc +1',
                  'jmp +4',
                  'acc +3',
                  'jmp -3',
                  'acc -99',
                  'acc +1',
                  'jmp -4',
                  'acc +6']

    print('PART 1')
    # TEST PART 1

    print('Test part 1')
    test_program = parse_program(test_input)
    test_result, test_acc = run_program(test_program)
    print('Test run_program, state',
          'RIGHT' if test_result == RESULT_INFINITE_LOOP_DETECTED
          else f'WRONG!! Expected {RESULT_INFINITE_LOOP_DETECTED} but was {test_result}')
    print('Test run_program, accumulator',
          'RIGHT' if test_acc == 5 else f'WRONG!! Expected 5 but was {test_acc}')

    # SOLVING PART 1
    sol_program = parse_program(sol_raw_program)
    sol_result, sol_acc = run_program(sol_program)

    print('SOLUTION PART 1', sol_acc)

    print('PART 2')
    test_repaired = repair_program(test_program)
    print('Test repair_program,'
          'RIGHT' if test_repaired == 8 else f'WRONG!! Expected 8 but was {test_repaired}')

    # SOLVE PART 2
    sol_repaired = repair_program(sol_program)
    print('SOLUTION PART 2', sol_repaired)
