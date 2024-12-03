# Day 3: Mull It Over
import re


def part1(lines):
    pattern = r'mul\((\d*\d*\d),(\d*\d*\d)\)'
    return sum([sum(map(lambda x: int(x[0]) * int(x[1]), list(re.findall(pattern, raw_data)))) for raw_data in lines])


def part2(lines):
    pattern = r"mul\((\d*\d*\d),(\d*\d*\d)\)|(do\(\))|(don't\(\))"
    compute_product = True
    result = 0
    for raw_data in lines:
        for left_factor, right_factor, we_do, we_do_not in re.findall(pattern, raw_data):
            if we_do != '':
                compute_product = True
            elif we_do_not != '':
                compute_product = False
            else:
                assert left_factor != '', 'left_factor is not a number'
                assert right_factor != '', 'right_factor is not a number'
                if compute_product:
                    result += int(left_factor) * int(right_factor)
    return result


if __name__ == '__main__':
    with open('data/aoc2024-input-day03.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    print('>>>>SOLUTION: ', part1(sol_raw_data))

    print('PART 2')
    print('>>>>SOLUTION: ', part2(sol_raw_data))
