# Day 11: Monkey in the Middle
import operator
from collections import namedtuple, defaultdict
import re
from functools import reduce, lru_cache

Monkey = namedtuple("Monkey", "id items operation_fun divisible_by test_true test_false")
Operation = namedtuple("Operation", "left_side operator right_side")


def parse_input(raw):
    def parse_fun(str_fun):
        parts = str_fun.split(' ')
        return Operation(parts[2], parts[3], parts[4])

    monkeys = []
    for x in range(0, len(raw), 7):
        str_monkey = '#'.join(raw[x:x + 7])
        regex = r"Monkey (\d):#  Starting items: ([^#]+)#  Operation: ([^#]+)#  Test: divisible by ([^#]+)" \
                r"#    If true: throw to monkey (\d)#    If false: throw to monkey (\d)"

        matches = re.match(regex, str_monkey)
        reg_data = matches.groups()
        items = [x for x in map(int, reg_data[1].split(', '))]
        operation = parse_fun(reg_data[2])
        monkey = Monkey(int(reg_data[0]), items, operation, int(reg_data[3]), int(reg_data[4]), int(reg_data[5]))
        monkeys.append(monkey)
    return monkeys


@lru_cache(maxsize=1000)
def calculate_new_worry_p1(old, fun):
    b = old if fun[2] == 'old' else int(fun[2])
    return old * b if fun[1] == '*' else old + b


@lru_cache(maxsize=1000)
def is_divisible_p1(new_worry, divisible_by):
    return new_worry % divisible_by == 0


def get_active_monkeys(monkeys, turns, calculate_worry_fun, divisible_fun, apply_relief, n_most_active=2, verbose=True):
    def do_round():
        monkeys_dir = {monkey.id: monkey for monkey in monkeys}
        inspects = defaultdict(lambda: 0)
        for monkey in monkeys:
            if verbose:
                print(f'MONKEY {monkey.id} -> {monkey.items}')
            while len(monkey.items) > 0:
                item = monkey.items.pop(0)
                new_worry = calculate_worry_fun(item, monkey.operation_fun)
                if verbose:
                    print('new worry (after fun)', new_worry)
                if apply_relief:
                    new_worry //= 3
                if verbose:
                    print('new worry (monkey bored)', new_worry)
                inspects[monkey.id] += 1
                if divisible_fun(new_worry, monkey.divisible_by):
                    monkeys_dir[monkey.test_true].items.append(new_worry)
                else:
                    monkeys_dir[monkey.test_false].items.append(new_worry)
        if verbose:
            for monkey in monkeys:
                print(monkey)
        return dict(inspects)

    inspections = {monkey.id: 0 for monkey in monkeys}

    for i in range(turns):
        iter_inspections = do_round()
        for k, v in iter_inspections.items():
            if k not in inspections:
                inspections[k] = v
            else:
                inspections[k] += v
        if verbose:
            print(f'round {i} inspections {iter_inspections} total inspections {inspections}')

    l = [(k, v) for k, v in inspections.items()]
    l.sort(key=lambda a: a[1], reverse=True)
    return l[:n_most_active]


def convert_monkeys(monkeys):
    def get_m_values():
        return [m.divisible_by for m in monkeys]

    m_values = get_m_values()
    for monkey in monkeys:
        n_items = len(monkey.items)
        for _ in range(n_items):
            item = monkey.items.pop(0)
            d_items = {}
            for m in m_values:
                d_items[m] = item % m
            monkey.items.append(d_items)
    return monkeys


def calculate_new_worry_p2(old, fun):
    b = old if fun[2] == 'old' else int(fun[2])
    m_values = old.keys()
    if isinstance(b, int):
        d_items = {}
        for m in m_values:
            d_items[m] = b % m
        b = d_items
    if fun[1] == '+':
        for k in b:
            old[k] += b[k]
    else:
        for k in b:
            old[k] *= b[k]
    for m in m_values:
        old[m] = old[m] % m
    return old


def is_divisible_p2(new_worry, divisible_by):
    return new_worry[divisible_by] == 0


if __name__ == '__main__':
    with open('data/aoc2022-input-day11.txt', 'r') as f:
        raw_data = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    data = parse_input(raw_data)
    m = get_active_monkeys(data, 20, calculate_new_worry_p1, is_divisible_p1, True, 2, verbose=False)
    ss = reduce(operator.mul, (d[1] for d in m))
    print('>>>SOLUTION: ', ss)

    print('PART 2')
    data = parse_input(raw_data)
    data = convert_monkeys(data)
    m = get_active_monkeys(data, 10000, calculate_new_worry_p2, is_divisible_p2, False, 2, verbose=False)
    ss = reduce(operator.mul, (d[1] for d in m))
    print('>>>SOLUTION: ', ss)
