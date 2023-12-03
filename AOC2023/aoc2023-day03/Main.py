# Day 3: Gear Ratios
import operator
import re
from functools import reduce
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass(eq=True)
class Number:
    value: int
    left: int
    right: int
    line: int

    def get_parts_from(self, symbols):
        return [s for s in symbols
                if (self.line - 1 <= s.line <= self.line + 1) and (self.left - 1 <= s.pos <= self.right + 1)]


class Symbol:
    glyph: str
    pos: int
    line: int
    id: int
    numbers: List[int]

    def __init__(self, id_symbol: int, glyph: str, pos: int, line: int, numbers: Optional[List[int]] = None):
        self.numbers = [] if numbers is None else numbers
        self.id = id_symbol
        self.glyph = glyph
        self.pos = pos
        self.line = line

    def __repr__(self):
        return f'Sym(id: {self.id}, glyph: {self.glyph}, pos: {self.pos}, line: {self.line}, numbers: {self.numbers})'

    def __eq__(self, other):
        return self.id == other.id and self.glyph == other.glyph and self.pos == other.pos and self.line == other.line

    def is_gear_symbol(self):
        return self.glyph == '*'


def parse_input(raw_data: List[str]) -> Tuple[List[Number], List[Symbol]]:
    reg_numbers = re.compile('([0-9]+)')
    reg_symbols = re.compile('([^.0-9])')
    all_numbers = []
    all_symbols = []
    n_symbol = 1
    for i, line in enumerate(raw_data):
        numbers = re.finditer(reg_numbers, line)
        for number in numbers:
            left = number.start()
            right = number.end()
            val = int(line[left:right])
            num = Number(value=val, line=i, left=left, right=right - 1)
            all_numbers.append(num)
        symbols = re.finditer(reg_symbols, line)
        for symbol in symbols:
            left = symbol.start()
            right = symbol.end()
            val = line[left:right]
            sym = Symbol(id_symbol=n_symbol, glyph=val, pos=left, line=i)
            n_symbol = n_symbol + 1
            all_symbols.append(sym)
    return all_numbers, all_symbols


# PART 1 & 2
def divide_parts(numbers: List[Number], symbols: List[Symbol]) -> Tuple[List[Number], List[Number], List[Symbol]]:
    part_numbers = []
    other_numbers = []
    potential_gears = {}
    for number in numbers:
        parts = number.get_parts_from(symbols)
        if any(parts):
            part_numbers.append(number)
            for p in parts:
                if p.is_gear_symbol():
                    p.numbers.append(number.value)
                    if p.id not in potential_gears:
                        potential_gears[p.id] = p
        else:
            other_numbers.append(number)

    real_gears = [gear for _, gear in potential_gears.items() if len(gear.numbers) == 2]

    return part_numbers, other_numbers, real_gears


def part1(part_numbers: List[Number]) -> int:
    return sum([n.value for n in part_numbers])


def part2(gears: List[Symbol]) -> int:
    return sum([reduce(operator.mul, gear.numbers) for gear in gears])


if __name__ == '__main__':
    with open('data/aoc2023-input-day03.txt', 'r') as f:
        sol_data = [line.strip('\n') for line in f.readlines()]

    sol_nums, sol_symbols = parse_input(sol_data)
    sol_pp, sol_oo, sol_gg = divide_parts(sol_nums, sol_symbols)

    print('PART 1')
    print('>>>>SOLUTION: ', part1(sol_pp))

    print('PART 2')
    print('>>>>SOLUTION: ', part2(sol_gg))
