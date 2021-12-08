# Day 8: Seven Segment Search

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
#
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

from collections import defaultdict
from typing import List, Dict

from Token import Token


def parse_input(raw_line: str):
    data = map(lambda x: x.strip(), raw_line.split('|'))
    data = map(lambda x: x.split(' '), data)
    data = [list(map(Token, x)) for x in data]
    return data


def count_tokens_with_length_at(lines: List[List[List[Token]]], segment_lengths: Dict[int, List[int]], position: int) \
        -> List[int]:
    search_segments = [k for k, v in segment_lengths.items() if len(v) == 1]
    return [token.cnt_segments()
            for line in lines
            for token in line[position]
            if token.cnt_segments() in search_segments]


def solve_line(line: List[List[Token]]) -> int:
    tokens = line[0]
    numbers = line[1]

    # Grouping every input pattern by its length.
    mapping = defaultdict(list)
    for token in tokens:
        mapping[token.cnt_segments()].append(token)

    # Obtaining every digit:
    # Digits 1, 4, 7, and 8 are automatically determined because they are the only patterns with a known length
    digit_1 = mapping[2][0].set_token_value(1)
    digit_4 = mapping[4][0].set_token_value(4)
    digit_7 = mapping[3][0].set_token_value(7)
    digit_8 = mapping[7][0].set_token_value(8)
    # print('(1):', digit_1, '(4):', digit_4, '(7):', digit_7, '(8):', digit_8)

    # Digits 6, 9 and 0. All of them patterns of length 6
    # - Digit 6 is the only member of length 6 which does not fully intersect with segments of digit 1
    # - Digit 9 is the member of length 6 which is not digit 6 and fully intersects with segments of digit 4
    # - Digit 0 is the remaining member of length 6
    digit_6 = [token for token in mapping[6] if
               len(set(token.signals).intersection(set(digit_1.signals))) == 1][0].set_token_value(6)
    digit_9 = [token for token in mapping[6] if
               token != digit_6
               and set(token.signals).intersection(set(digit_4.signals)) == set(digit_4.signals)][0].set_token_value(9)
    digit_0 = [token for token in mapping[6] if token != digit_6 and token != digit_9][0].set_token_value(0)
    # print('(6):', digit_6, '(9):', digit_9, '(0):', digit_0)

    # Digits 2, 3, and 5. All of them patterns of length 5
    # - Digit 5 is the only member of length 5 that does not have active the top right segment
    #       - The top-right segment is the segment of digit 1 not active in digit 6
    # - Digit 2 is the member of length 5 that is not digit 5 and has active all segments of digit 4
    # - Digit 3 is the remaining member of length 5
    segment_top_right = [signal for signal in digit_1.signals if signal not in digit_6.signals][0]
    digit_5 = [token for token in mapping[5] if segment_top_right not in token.signals][0].set_token_value(5)
    digit_2 = [token for token in mapping[5] if
               token != digit_5 and len(set(token.signals).intersection(set(digit_1.signals))) == 1][0].set_token_value(
        2)
    digit_3 = [token for token in mapping[5] if token != digit_5 and token != digit_2][0].set_token_value(3)
    # print('(5):', digit_5, '(2):', digit_2, '(3):', digit_3)

    digits = [digit_1, digit_2, digit_3, digit_4, digit_5, digit_6, digit_7, digit_8, digit_9, digit_0]

    # OK, obtaining the 4 digit result
    base = 1000
    result = 0
    for number in numbers:
        result += base * [token.value for token in digits if token.signals == number.signals][0]
        base //= 10

    return result


def solve_lines(lines: List[List[List[Token]]]) -> int:
    result = 0
    for line in lines:
        result += solve_line(line)
    return result


if __name__ == '__main__':
    with open('data/aoc2021-input-day08.txt', 'r') as f:
        sol_raw_instructions = [line.strip('\n') for line in f.readlines()]

    # PART 1:
    print('PART 1:')
    sol_instructions = list(map(parse_input, sol_raw_instructions))
    sol_special = count_tokens_with_length_at(sol_instructions, Token.special_lengths, 1)
    print('>>>SOLUTION:', len(sol_special))

    # PART 2:
    print('PART 2:')
    print('>>>SOLUTION:', solve_lines(sol_instructions))
