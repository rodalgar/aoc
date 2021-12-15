# Day 12: Passage Pathing
from __future__ import annotations

import copy
from collections import deque, Counter
from typing import List, Dict, Deque, Tuple

from Node import Node


def parse_input(raw_paths: List[str]) -> Dict[str, Node]:
    nodes = {}
    for raw_path in raw_paths:
        slices = raw_path.split('-')
        left = slices[0]
        right = slices[1]
        if left not in nodes:
            nodes[left] = Node(left)
        if right not in nodes:
            nodes[right] = Node(right)
        nodes[left].add_adjacent(nodes[right])
        nodes[right].add_adjacent(nodes[left])
    return nodes


def check_small_caves_only_once(nodes, adjacent: Node, actual_path: Deque) -> bool:
    return adjacent.symbol in actual_path


def find_paths(nodes: Dict[str, Node], check_small_caves_fub) -> Tuple[int, List]:
    def recursive_find_paths(actual_node: Node, actual_path: Deque, paths: List[Deque], check_small_caves):
        for adjacent in actual_node.adjacent_nodes:
            if adjacent.is_small_cave() and check_small_caves(nodes, adjacent, actual_path):
                continue
            new_path = copy.deepcopy(actual_path)
            new_path.append(adjacent.symbol)
            if adjacent.symbol == 'end':
                paths.append(new_path)
            else:
                recursive_find_paths(adjacent, new_path, paths, check_small_caves)

    start_node = nodes['start']
    first_path = deque()
    all_paths = []

    first_path.append(start_node.symbol)

    recursive_find_paths(start_node, first_path, all_paths, check_small_caves_fub)

    return len(all_paths), all_paths


def check_small_caves_at_most_two(nodes, adjacent: Node, actual_path: Deque) -> bool:
    if adjacent.symbol in ['start', 'end']:
        return check_small_caves_only_once(nodes, adjacent, actual_path)
    c = Counter([symbol for symbol in actual_path if nodes[symbol].is_small_cave()])
    if adjacent.symbol not in c:
        return False
    times_adjacent_already_in = c[adjacent.symbol]
    if times_adjacent_already_in == 2:
        return True

    return 2 in set(c.values())


if __name__ == '__main__':
    with open('data/aoc2021-input-day12.txt', 'r') as f:
        sol_raw_paths = [line.strip('\n') for line in f.readlines()]

    # PART 1
    print('PART 1:')
    n_paths, sol_paths = find_paths(parse_input(sol_raw_paths), check_small_caves_only_once)
    print('>>>SOLUTION:', n_paths, len(sol_paths))

    # PART 2
    print('PART 2:')
    n_paths, sol_paths = find_paths(parse_input(sol_raw_paths), check_small_caves_at_most_two)
    print('>>>SOLUTION:', n_paths, len(sol_paths))
