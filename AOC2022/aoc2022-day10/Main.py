# Day 10: Cathode-Ray Tube
from collections import namedtuple

Instruction = namedtuple("Instruction", "code cycles_needed desc")
OPCODE_NOOP = 1
OPCODE_ADDX = 2
INST_NOOP = Instruction(code=OPCODE_NOOP, cycles_needed=1, desc='NOOP')
INST_ADDX = Instruction(code=OPCODE_ADDX, cycles_needed=2, desc='ADDX')


def parse_input(raw):
    instructions = []
    for line in raw:
        parts = line.split(' ')
        assert parts[0] in ['noop', 'addx'], f'Instruction {parts[0]} unknown!'
        if len(parts) == 1:
            instructions.append((INST_NOOP, None))
        else:
            instructions.append((INST_ADDX, int(parts[1])))
    return instructions


def execute(program, extract_at=[], verbose=False):
    clock = 1
    register_x = 1
    extractions = []
    CRT_line = ''
    CRT = []
    for instruction in program:
        counter = instruction[0].cycles_needed
        while counter > 0:
            if verbose:
                print(f'INIT clock: {clock} executing: {instruction[0].desc} register_x: {register_x}')
            counter -= 1
            if clock in extract_at:
                extractions.append((clock, register_x))
            n_pixel = len(CRT_line)
            if register_x - 1 <= n_pixel <= register_x + 1:
                CRT_line += '#'
            else:
                CRT_line += '.'

            if counter == 0:
                if instruction[0].code == OPCODE_ADDX:
                    register_x += instruction[1]
            if verbose:
                print(f'END clock: {clock} executing: {instruction[0].desc} register_x: {register_x}')
            clock += 1
            if len(CRT_line) == 40:
                CRT.append(CRT_line)
                CRT_line = ''
    return register_x, extractions, CRT


if __name__ == '__main__':
    with open('data/aoc2022-input-day10.txt', 'r') as f:
        raw_data = [line.strip('\n') for line in f.readlines()]

    spr = parse_input(raw_data)
    print('PART 1')
    reg, extr, crt = execute(spr, [20, 60, 100, 140, 180, 220])
    print('>>>SOLUTION: ', sum(cycle * register_x for cycle, register_x in extr))

    print('PART 2')
    print('>>>SOLUTION: ', 'EKRHEPUZ')
    for line in crt:
        print(line)
