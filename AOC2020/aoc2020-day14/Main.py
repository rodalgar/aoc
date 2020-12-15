# Day 14: Docking Data
import re
import numpy as np

# PART 1
CMD_MASK = 0
CMD_MEM = 1


def build_mask(str_bits):
    """
    Transforms an string representing bits into a bit vector contained in an int value.

    :param str_bits: List of string representing bits.
    :return: int value
    """
    int_mask = 0
    for i, n_bit in enumerate(range(len(str_bits) - 1, -1, -1)):
        bit = int(str_bits[n_bit]) << i
        int_mask = int_mask | bit

    return int_mask


def parse_mask_v1(chunks):
    """
    Parses mask as per part 1 rules. Given an input string this will generate two masks. Mask0 that will be used as
    number & mask0 and Mask1 what will be used as number | mask1.

    :param chunks: Chopped instruction.
    :return: Tuple of command mask, mask0 and mask1.
    """
    if len(chunks) != 2:
        raise Exception(f'mask command malformed! Should have 2 chunks, has {len(chunks)}. {chunks}')

    raw_mask = chunks[1]
    # Mask0 (will be used as number & mask0)
    int_mask0 = build_mask(raw_mask.replace('X', '1'))

    # Mask1 (will be used as number | mask1)
    int_mask1 = build_mask(raw_mask.replace('X', '0'))

    return CMD_MASK, int_mask0, int_mask1


def parse_mem(chunks):
    """
    Parses a mem command. Obtains memory position and data both as int values.

    :param chunks: Chopped instruction.
    :return: Tuple of command mem, memory position and data
    """
    if len(chunks) != 2:
        raise Exception(f'mem command malformed! Should have 2 chunks, has {len(chunks)}. ({chunks})')
    result = re.findall("mem\[(\d+)\]", chunks[0])
    if result is None:
        raise Exception(f"mem command malformed! Can't find memory address! {chunks[0]}. ({chunks})")

    return CMD_MEM, int(result[0]), int(chunks[1])


def parse_program(raw_program, fun_parse_mask, fun_parse_mem):
    """
    Parses a list of string representing a program int a list of parsed commands.

    :param raw_program: List of string representing a program.
    :param fun_parse_mask: Function to apply when a mask command is found.
    :param fun_parse_mem: Function to apply when a mem command is found.
    :return:
    """
    program = []

    for line in raw_program:
        chunks = list(map(lambda x: x.strip(), line.split('=')))
        if chunks[0] == 'mask':
            command = fun_parse_mask(chunks)
        elif re.match("mem\[\d+\]", chunks[0]):
            command = fun_parse_mem(chunks)
        else:
            raise Exception(f'Unknown command {chunks[0]} ({line})')
        program.append(command)
    return program


def apply_mask(mask, data):
    """
    Applies a mask to data, following rules of part 1

    :param mask: Tuple of (mask0, mask1)
    :param data: Value
    :return: masked data.
    """
    # first mask0
    masked_data = data & mask[0]

    # then mask1
    masked_data = masked_data | mask[1]

    return masked_data


def write_to_memory(memo, mask, position, data):
    """
    Applies mask to a int value and stores it in memory at a given memory position.

    :param memo: Memory of program.
    :param mask: Mask to apply to data.
    :param position: Memory position to write data to.
    :param data: Int value to store in memory.
    :return: Modified memory.
    """
    # Apply mask to data
    masked_data = apply_mask(mask, data)

    # Write new data to memo at 'position'
    memo[position] = masked_data

    return memo


def run_program(program):
    """
    Executes a program with version v1.

    :param program: V1 Program to run.
    :return: memory state.
    """
    current_mask = None
    memory = {}

    for instruction in program:
        command = instruction[0]
        if command == CMD_MASK:
            # TODO: Check parameters?
            current_mask = (instruction[1], instruction[2])
        elif command == CMD_MEM:
            memory = write_to_memory(memory, current_mask, instruction[1], instruction[2])
        else:
            raise Exception(f'Unknown instruction {command}. ({instruction})')

    return memory


def sum_non_zero_values_in_memory(mem):
    """
    Sums all values stored in memory.

    :param mem: State of memory.
    :return: Sum of all values.
    """

    return sum(mem.values())


# PART 2
def execute_mem_v2(mem_address, mask):
    """
    Computes all memory addresses affected by mask

    :param mem_address: input memory possition.
    :param mask: mask to apply.
    :return: List of memory positions.
    """

    # Convert memory address to string, with leading zeroes to fill 36 positions.
    str_address = "{0:036b}".format(mem_address)
    direcs = np.zeros(0)

    for ix in range(len(mask) - 1, -1, -1):
        cha = mask[ix]
        if cha == 'X':  # Floating
            if direcs.shape[0] == 0:
                nuevo = np.empty(shape=(2, 1))
                nuevo[0][0] = '0'
                nuevo[1][0] = '1'
                direcs = nuevo
            else:
                direcs = np.vstack((direcs, direcs))
                nuevo = np.zeros(shape=(direcs.shape[0], 1))
                middle = direcs.shape[0] // 2
                nuevo[:middle] = '0'
                nuevo[middle:] = '1'
                direcs = np.hstack((nuevo, direcs))
        elif cha == '0':  # Unchanged
            if direcs.shape[0] == 0:
                direcs = np.zeros(shape=(1, 1))
                direcs[0] = str_address[ix]
            else:
                nuevo = np.zeros(shape=(direcs.shape[0], 1))
                nuevo.fill(str_address[ix])
                direcs = np.hstack((nuevo, direcs))
        elif cha == '1':  # overwritten with 1
            if direcs.shape[0] == 0:
                direcs = np.ones(shape=(1, 1))
            else:
                nuevo = np.ones(shape=(direcs.shape[0], 1))
                direcs = np.hstack((nuevo, direcs))

    # Convert all binary memory positions to integer
    outs = []
    for i in range(direcs.shape[0]):
        data = 0
        for id, ix in enumerate(range(len(mask) - 1, -1, -1)):
            int_bit = int(direcs[i][ix]) << id
            data = data | int_bit
        outs.append(data)

    return outs


def parse_mask_v2(chunks):
    """
    Parses mask as per part 2 rules

    :param chunks: Chopped instruction.
    :return: Tuple of mask command and mask
    """
    return CMD_MASK, chunks[1]


def run_program_v2(program):
    """
    Executes a program with version v2.

    :param program: V2 Program to run.
    :return: memory state.
    """

    current_mask = None
    memory = {}

    for instruction in program:
        command = instruction[0]
        if command == CMD_MASK:
            # TODO: Check parameters?
            current_mask = instruction[1]
        elif command == CMD_MEM:
            # Obtaining all memory addresses variations.
            direcs = execute_mem_v2(instruction[1], current_mask)
            for direc in direcs:
                memory[direc] = instruction[2]
        else:
            raise Exception(f'Unknown instruction {command}. ({instruction})')

    return memory


if __name__ == '__main__':
    with open('data/aoc2020-input-day14.txt', 'r') as f:
        sol_str_program = [line.strip('\n') for line in f.readlines()]

    test_raw_program = ['mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
                        'mem[8] = 11',
                        'mem[7] = 101',
                        'mem[8] = 0']

    test_raw_program_2 = ['mask = 000000000000000000000000000000X1001X',
                          'mem[42] = 100',
                          'mask = 00000000000000000000000000000000X0XX',
                          'mem[26] = 1']

    print('PART 1')
    # TEST PART 1
    test_program = parse_program(test_raw_program, parse_mask_v1, parse_mem)
    test_memory = run_program(test_program)
    test_result = sum_non_zero_values_in_memory(test_memory)
    print('Test part 1', 'RIGHT' if test_result == 165 else f'WRONG!! Expected 165 but was {test_result}')

    # SOLVING PART 1
    sol_program = parse_program(sol_str_program, parse_mask_v1, parse_mem)
    sol_memory = run_program(sol_program)
    sol_result = sum_non_zero_values_in_memory(sol_memory)
    print('SOLUTION PART 1', sol_result)
    print()

    print('PART 2')
    # TEST PART 2
    mask = '000000000000000000000000000000X1001X'
    mem_address = 42
    outs = execute_mem_v2(mem_address, mask)
    expected = [26, 27, 58, 59]
    print('Testing execute_mem_v2 (1)', 'RIGHT' if outs == expected else f'WRONG!! Expected {expected} but was {outs}')

    mask = '00000000000000000000000000000000X0XX'
    mem_address = 26
    outs = execute_mem_v2(mem_address, mask)
    expected = [16, 17, 18, 19, 24, 25, 26, 27]
    print('Testing execute_mem_v2 (2)', 'RIGHT' if outs == expected else f'WRONG!! Expected {expected} but was {outs}')

    test_program_2 = parse_program(test_raw_program_2, parse_mask_v2, parse_mem)
    test_memory_2 = run_program_v2(test_program_2)
    test_result_2 = sum_non_zero_values_in_memory(test_memory_2)
    print('Test part 2', 'RIGHT' if test_result_2 == 208 else f'WRONG!! Expected 208 but was {test_result}')

    # SOLVING PART 2
    sol_program_2 = parse_program(sol_str_program, parse_mask_v2, parse_mem)
    sol_memory_2 = run_program_v2(sol_program_2)
    sol_result_2 = sum_non_zero_values_in_memory(sol_memory_2)
    print('SOLUTION PART 2', sol_result_2)
