# Day 5: Supply Stacks


def parse_input(raw_input):
    reading_stacks = True
    reading_instructions = False
    yard = []
    instructions = []
    for line in raw_input:
        if reading_stacks:
            for i in range(0, len(line), 4):
                crate = line[i:i + 4]
                stack = (i // 4)
                if stack == len(yard):
                    yard.append([])

                if crate[0] == '[':
                    crate = crate[1]
                    yard[stack].append(crate)
                elif ' 1' in crate:
                    reading_stacks = False
        elif len(line) == 0:
            reading_instructions = True
        elif reading_instructions:
            parts = line.split(' ')
            instructions.append((int(parts[1]), int(parts[3]) - 1, int(parts[5]) - 1))

    return yard, instructions


def move_things(yard, instructions, reverse_items=True):
    for inst in instructions:
        qtty = inst[0]
        opos = inst[1]
        tpos = inst[2]
        origin = yard[opos]
        merch = origin[:qtty]
        if reverse_items:
            merch.reverse()
        # remove
        yard[opos] = yard[opos][qtty:]
        # put
        yard[tpos] = merch + yard[tpos]

    return yard


def get_tops(yard):
    return ''.join([pile[0]
                    for pile in yard])


if __name__ == '__main__':
    with open('data/aoc2022-input-day05.txt', 'r') as f:
        raw_data = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    data = parse_input(raw_data)
    d = move_things(data[0], data[1])
    print('>>>SOLUTION: ', get_tops(d))

    print('PART 2')
    data = parse_input(raw_data)
    d = move_things(data[0], data[1], reverse_items=False)
    print('>>>SOLUTION: ', get_tops(d))
