# Day 11: Plutonian Pebbles
from collections import Counter, defaultdict


def parse_input(raw_data: str) -> [str]:
    return raw_data.split()


def blink_compact(dict_data: {str: int}) -> {str: int}:
    new_num_items = defaultdict(int)

    new_data = []
    for item in dict_data:
        if item == '0':
            new_data.append(('1', dict_data[item]))
        elif len(item) % 2 == 0:
            left = item[:int(len(item) / 2)].lstrip('0') or '0'
            right = item[int(len(item) / 2):].lstrip('0') or '0'
            new_data.append((left, dict_data[item]))
            new_data.append((right, dict_data[item]))
        else:
            new_data.append((str(int(item) * 2024), dict_data[item]))

    for item, repetitions in new_data:
        new_num_items[item] += repetitions
    return new_num_items


def blink_compact_init(data: [str], iterations: int = 1) -> ({str: int}, int):
    # observation 1: Each term is independent of the others. We can process the list in any order
    # observation 2: Different occurrences of the same term behave exactly the same, so we can process it
    # only once and "multiply" by the number of occurrences. We will "compact" the initial list and repeat
    # that after each iteration so the next one only processes each term only once.
    c = Counter(data)

    for _ in range(iterations):
        c = blink_compact(c)

    return c, sum(c.values())


if __name__ == '__main__':
    with open('data/aoc2024-input-day11.txt', 'r') as f:
        sol_raw_data = f.readline()

    sol_data = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', blink_compact_init(sol_data, 25)[1])

    print('PART 2')
    print('>>>>SOLUTION: ', blink_compact_init(sol_data, 75)[1])
