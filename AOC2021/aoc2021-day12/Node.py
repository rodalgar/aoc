from __future__ import annotations
from typing import List


class Node:
    symbol: str
    adjacent_nodes: List[Node]

    def __init__(self, symbol):
        self.symbol = symbol
        self.adjacent_nodes = []

    def add_adjacent(self, adjacent: Node):
        self.adjacent_nodes.append(adjacent)

    def is_small_cave(self):
        return self.symbol[0].islower()

    def __repr__(self):
        adjacent_symbols = [a.symbol for a in self.adjacent_nodes]
        return f"({self.symbol} -> {','.join(adjacent_symbols)})"
