# Day 3: Rucksack Reorganization
import string

priorities = {k: i for i, k in enumerate(string.ascii_letters, start=1)}


def parse_input(raw_data_in):
    return [[rucksack[:(len(rucksack) // 2)], rucksack[(len(rucksack) // 2):], rucksack]
            for rucksack in raw_data_in]


# PART 1
def get_misplaced_item(data_in):
    return [priorities[intersection]
            for rucksack in data_in
            for intersection in set(rucksack[0]) & set(rucksack[1])]


# PART 2
def get_group_badges(data_in):
    return [priorities[intersection]
            for group in (data_in[x:x + 3]
                          for x in range(0, len(data_in), 3))
            for intersection in set(group[0][2]) & set(group[1][2]) & set(group[2][2])]


if __name__ == '__main__':
    with open('data/aoc2022-input-day03.txt', 'r') as f:
        raw_data = [line.strip('\n') for line in f.readlines()]

        data = parse_input(raw_data)

        print('PART 1')
        print('>>>SOLUTION: ', sum(get_misplaced_item(data)))

        print('PART 2')
        print('>>>SOLUTION: ', sum(get_group_badges(data)))
