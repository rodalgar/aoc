# DAY 7: Handy Haversacks
import re


# PART 1
class Bag:
    code = None
    contained_by = None
    bag_code_contains = None
    bag_contains = None

    def __init__(self, code):
        self.code = code
        self.contained_by = []
        self.bag_code_contains = []
        self.bag_contains = []

    def __repr__(self):
        return f'**code {self.code} bag_code_contains {self.bag_code_contains} contained_by {self.contained_by}**'

    def deep_recursive_contained(self, must_sum_yourself=False):
        counted = 1 if must_sum_yourself else 0
        for qty, contained_bag in self.bag_contains:
            counted += (qty * contained_bag.deep_recursive_contained(must_sum_yourself=True))
        return counted


def parse_bag(raw_input):
    """
    Parses a single bag from a string.

    :param raw_input: String representing a bag.
    :return: Bag object.
    """
    # drab plum bags contain 5 clear turquoise bags, 5 striped aqua bags, 4 dotted gold bags, 4 plaid chartreuse bags.
    # Parsing origin bag
    print('PARSING', raw_input)
    regexp_pattern_bag = "(.+) bags? contain"
    result = re.findall(regexp_pattern_bag, raw_input)
    assert result is not None, f"Bad parsing!, can't find origin bag {raw_input}"
    bag = Bag(result[0])

    # Parsing contained inside
    regexp_pattern_contains = "(\d) ([^ ]+? [^ ]+?) bag"
    res = re.findall(regexp_pattern_contains, raw_input)
    if len(res) > 0:
        for qty, dep in res:
            bag.bag_code_contains.append((int(qty), dep))

    return bag


def parse_rules(raw_input):
    """
    Transforms a list of instructions into a list of Bag objects. With relationships 'contain' and 'contained_by' with
    other bags.

    :param raw_input: List of instructions.
    :return: List of Bag.
    """

    # parsed_bags = list(map(parse_bag, raw_input))
    bags = {bag.code: bag for bag in map(parse_bag, raw_input)}

    # as all bags al processed now, we fill the (directly) "contained_by" relationship
    for code, bag in bags.items():
        print(bag)
        for qty, contained in bag.bag_code_contains:
            print('\t', code, 'bag_code_contains', contained)
            contained_bag = bags[contained]
            contained_bag.contained_by.append(code)
            bag.bag_contains.append((qty, contained_bag))

    return bags


def deep_contained_in(bags, bag_code, verbose=False):
    """
    Traverses contained_by relationship of a list of bags to find out which ones contain a given one directly
    or indirectly.

    :param verbose: if True prints some debugging info.
    :param bags: List of bags.
    :param bag_code: bag code which contained status we want to know.
    :return: set of bag codes which contain bag_code.
    """

    already_processed_bag = set()
    # although is not necessary we traverse relationships in order... just in case, wink wink
    processing_queue = []
    container_bags = set()
    # first element is initial bag code. Queue it, and mark it.
    processing_queue.append(bag_code)
    already_processed_bag.add(bag_code)
    while len(processing_queue) > 0:
        # dequeue item
        actual_bag_code = processing_queue[:1][0]
        processing_queue = processing_queue[1:]
        if verbose:
            print('Processing', actual_bag_code)

        actual_bag = bags[actual_bag_code]
        for contained_in_bag in actual_bag.contained_by:
            if contained_in_bag not in already_processed_bag:
                if verbose:
                    print('\tAdding to queue', contained_in_bag)
                processing_queue.append(contained_in_bag)
                container_bags.add(contained_in_bag)
                already_processed_bag.add(contained_in_bag)
        if verbose:
            print('\t\tStatus!')
            print('\t\t\tprocessing_queue', processing_queue)
            print('\t\t\talready_processed_bag', already_processed_bag)
            print('\t\t\tcontainer_bags', container_bags)

    return container_bags


if __name__ == '__main__':
    with open('data/aoc2020-input-day07.txt', 'r') as f:
        sol_rules = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    # TEST PART 1
    test_sample = 'drab plum bags contain 5 clear turquoise bags, 5 striped aqua bags,' \
                  ' 4 dotted gold bags, 4 plaid chartreuse bags.'

    test_rules = [
        'light red bags contain 1 bright white bag, 2 muted yellow bags.',
        'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
        'bright white bags contain 1 shiny gold bag.',
        'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
        'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
        'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
        'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
        'faded blue bags contain no other bags.',
        'dotted black bags contain no other bags.'
    ]

    test_bag = parse_bag(test_sample)
    test_bags = parse_rules(test_rules)
    print('Testing parse_bag', 'RIGHT' if test_bag is Bag and test_bag.code == 'drab plum' else f'WRONG!!')
    print('Testing parse_rules',
          'RIGHT' if len(test_bags) == 7 else f'WRONG!! Was {len(test_bags)} but 7 was expected.')

    test_deep = len(deep_contained_in(test_bags, 'shiny gold'))
    print('Testing deep_contained_in', 'RIGHT' if test_deep == 4 else f'WRONG!! Was {test_deep} but 4 was expected.')

    # SOLVING PART 1
    sol_bags = parse_rules(sol_rules)
    sol_part_1 = deep_contained_in(sol_bags, 'shiny gold')
    print('SOLUTION PART 1', len(sol_part_1))

    print()
    print('PART 2')
    # TEST PART 2
    test_rules_part2 = ['shiny gold bags contain 2 dark red bags.',
                        'dark red bags contain 2 dark orange bags.',
                        'dark orange bags contain 2 dark yellow bags.',
                        'dark yellow bags contain 2 dark green bags.',
                        'dark green bags contain 2 dark blue bags.',
                        'dark blue bags contain 2 dark violet bags.',
                        'dark violet bags contain no other bags.']

    test_bags_part2 = parse_rules(test_rules_part2)
    test_bag = test_bags_part2['shiny gold']
    test_recursive = test_bag.deep_recursive_contained()
    print('Testing Bag.deep_recursive_contained',
          'RIGHT' if test_recursive == 5 else f'WRONG!! Was {test_recursive} but 5 was expected.')

    # SOLVING PART 2
    sol_bag = sol_bags['shiny gold']
    print('SOLUTION PART 2', sol_bag.deep_recursive_contained())
