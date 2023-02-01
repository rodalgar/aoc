# Day 9: Rope Bridge

DIR_UP = (-1, 0)
DIR_RIGHT = (0, 1)
DIR_DOWN = (1, 0)
DIR_LEFT = (0, -1)


def parse_input(raw):
    def parse_direction(d):
        assert d in ['U', 'R', 'D', 'L'], f'DIRECTION {d} IS UNKNOWN!'
        if d == 'U':
            return DIR_UP
        elif d == 'R':
            return DIR_RIGHT
        elif d == 'D':
            return DIR_DOWN
        else:
            return DIR_LEFT

    instructions = []
    for line in raw:
        parts = line.split(' ')
        instructions.append((parse_direction(parts[0]), int(parts[1])))
    return instructions


def move_rope(instructions, n_knots=2):
    def move_head(direction):
        return direction[0] + head[0], direction[1] + head[1]

    def move_knot(knot, next_knot):
        # should I move?
        if abs(knot[0] - next_knot[0]) <= 1 and abs(knot[1] - next_knot[1]) <= 1:
            return knot

        # ok ok, moving out...
        if next_knot[0] > knot[0]:
            knot = (knot[0] + 1, knot[1])
        elif next_knot[0] < knot[0]:
            knot = (knot[0] - 1, knot[1])

        if next_knot[1] > knot[1]:
            knot = (knot[0], knot[1] + 1)
        elif next_knot[1] < knot[1]:
            knot = (knot[0], knot[1] - 1)

        return knot

    head = (0, 0)
    knots = [(0, 0) for _ in range(n_knots - 1)]
    tail_visited = set()

    tail_visited.add(knots[-1])
    for instruction in instructions:
        for _ in range(instruction[1]):
            head = move_head(instruction[0])
            last_knot = head
            for i in range(n_knots - 1):
                knots[i] = move_knot(knots[i], last_knot)
                last_knot = knots[i]
            tail_visited.add(last_knot)

    return tail_visited


if __name__ == '__main__':
    with open('data/aoc2022-input-day09.txt', 'r') as f:
        raw_data = [line.strip('\n') for line in f.readlines()]

    data = parse_input(raw_data)

    print('PART 1')
    print('>>>SOLUTION: ', len(move_rope(data)))

    print('PART 2')
    print('>>>SOLUTION: ', len(move_rope(data, 10)))
