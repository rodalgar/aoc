# Day 4: Camp Cleanup


def parse_input(raw_data_in):
    elves = []
    for line in raw_data_in:
        pair = []
        chunks = line.split(',')
        for i in range(2):
            borders = chunks[i].split('-')
            pair.append(range(int(borders[0]), int(borders[1]) + 1))
        elves.append(pair)
    return elves


# PART 1
def find_full_overlaps(assignments):
    return [pair
            for pair in assignments
            if (pair[0].start in pair[1] and pair[0][-1] in pair[1])
            or (pair[1].start in pair[0] and pair[1][-1] in pair[0])]


# PART 2
def find_overlaps(assignments):
    return [pair
            for pair in assignments
            if len(set(pair[0]) & set(pair[1])) > 0]


if __name__ == '__main__':
    with open('data/aoc2022-input-day04.txt', 'r') as f:
        raw_data = [line.strip('\n') for line in f.readlines()]

    data = parse_input(raw_data)

    print('PART 1')
    print('>>>SOLUTION: ', len(find_full_overlaps(data)))

    print('PART 2')
    print('>>>SOLUTION: ', len(find_overlaps(data)))
