# Day 14: Extended Polymerization
from collections import Counter
from functools import lru_cache
from typing import List, Dict


def parse_input(raw_data: List[str]):
    template = raw_data[0]

    rules = {d[0]: d[1] for d in map(lambda x: x.split(' -> '), raw_data[2:])}
    return template, rules


def apply_steps_rec_v3(template_in: str, rules_in: Dict[str, str], n_steps: int) -> int:
    """
        We will slice the input template in pairs. These pairs are always consecutive.

        Then we obtain the transformation between them and put the new one in the middle thus
         obtaining two new consecutive pair, and we go on like that recursively until a depth level
         equal as the steps required.

         Because the actual sentence is not required we count instead the occurring symbols

         Mmm... As we go preorder it should not be too hard to reconstruct the entire sentence
         should it be needed.
    :param template_in: starting template
    :param rules_in: pair insertion rules
    :param n_steps: steps of pair insertion to perform
    :return: difference between the most common element and the least common element
    """
    @lru_cache(maxsize=None)
    def recursion(left_symbol: str, right_symbol: str, depth: int, max_depth: int):
        if depth == max_depth:
            return Counter(left_symbol)
        else:
            new_char = rules_in[left_symbol + right_symbol]
            c1 = recursion(left_symbol, new_char, depth + 1, max_depth)
            c2 = recursion(new_char, right_symbol, depth + 1, max_depth)

            c3 = Counter(c1)
            c3.update(c2)
            return c3

    counter = Counter()
    for index in range(len(template_in) - 1):
        dataa = recursion(template_in[index], template_in[index + 1], 0, n_steps)
        counter.update(dataa)

    # As there is overlapping between the edge symbols in a pair and the next one we treated all pairs as
    # an open interval to the right, so in case of overlapping the edge symbol is only counted once. The
    # backside of this is that the last element of the original template is not counted, so we count it
    # now
    counter.update(template_in[-1])

    # Alright boys, them elements are counted, so we answer the question
    elements = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    most = elements[0]
    least = elements[-1]

    # 'most' and 'least' have the counted information as well as the symbol
    return most[1] - least[1]


if __name__ == '__main__':
    with open('data/aoc2021-input-day14.txt', 'r') as f:
        sol_raw_instructions = [line.strip('\n') for line in f.readlines()]

    # PART 1
    sol_template, sol_rules = parse_input(sol_raw_instructions)
    sol_foo = apply_steps_rec_v3(sol_template, sol_rules, 10)
    print('PART 1')
    print('>>>SOLUTION:', sol_foo)

    sol_template, sol_rules = parse_input(sol_raw_instructions)
    sol_foo = apply_steps_rec_v3(sol_template, sol_rules, 40)
    print('PART 2')
    print('>>>SOLUTION:', sol_foo)
