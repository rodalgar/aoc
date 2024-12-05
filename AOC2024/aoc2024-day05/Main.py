# Day 5: Print Queue

def parse_input(raw_data: [str]) -> ({int: set[int]}, [[int]]):
    rules = {}
    updates = []
    reading_rules = True
    for line in raw_data:
        if len(line) == 0:
            reading_rules = False
            continue

        if reading_rules:
            data = list(map(int, line.split('|')))
            if not data[0] in rules:
                rules[data[0]] = {data[1]}
            else:
                rules[data[0]].add(data[1])
        else:
            updates.append(list(map(int, line.split(','))))

    for update in updates:
        for page in update:
            if page not in rules:
                rules[page] = set()

    return rules, updates


# PART 1
def check_correct_update(rules: {int: set[int]}, update: [int]) -> bool:
    for ix_page in range(len(update) - 1):
        page = update[ix_page]
        next_pages = rules[page]
        if not update[ix_page + 1] in next_pages:
            return False
    return True


def get_correct_updates(rules: {int: set[int]}, updates: [[int]]) -> [[int]]:
    return [update for update in updates if check_correct_update(rules, update)]


def part1(rules: {int: set[int]}, updates: [[int]]) -> int:
    correct_updates = get_correct_updates(rules, updates)
    data = [update[(len(update) // 2)] for update in correct_updates]
    return sum(data)


# PART 2
def get_incorrect_updates(rules: {int: set[int]}, updates: [[int]]) -> [[int]]:
    return [update for update in updates if not check_correct_update(rules, update)]


def fix_update(rules: {int: set[int]}, original_update: [int]) -> [int]:
    ix_page = 0
    update = original_update.copy()
    while ix_page < len(update) - 1:
        page = update[ix_page]
        next_pages = rules[page]
        if not update[ix_page + 1] in next_pages:
            update[ix_page] = update[ix_page + 1]
            update[ix_page + 1] = page
            ix_page = 0
            continue
        ix_page += 1
    return update


def part2(rules: {int: set[int]}, updates: [[int]]) -> int:
    incorrect_updates = get_incorrect_updates(rules, updates)
    fixed_updates = [fix_update(rules, update) for update in incorrect_updates]
    data = [update[(len(update) // 2)] for update in fixed_updates]
    return sum(data)


if __name__ == '__main__':
    with open('data/aoc2024-input-day05.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_rules, sol_updates = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', part1(sol_rules, sol_updates))

    print('PART 2')
    print('>>>>SOLUTION: ', part2(sol_rules, sol_updates))
