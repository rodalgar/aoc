from collections import deque

import pytest

from Main import parse_input, check_small_caves_only_once, check_small_caves_at_most_two, find_paths
from Node import Node

raw_test_data_1 = [
    'start-A',
    'start-b',
    'A-c',
    'A-b',
    'b-d',
    'A-end',
    'b-end'
]

raw_test_data_2 = [
    'dc-end',
    'HN-start',
    'start-kj',
    'dc-start',
    'dc-HN',
    'LN-dc',
    'HN-end',
    'kj-sa',
    'kj-HN',
    'kj-dc'
]

raw_test_data_3 = [
    'fs-end',
    'he-DX',
    'fs-he',
    'start-DX',
    'pj-DX',
    'end-zg',
    'zg-sl',
    'zg-pj',
    'pj-he',
    'RW-he',
    'fs-DX',
    'pj-RW',
    'zg-RW',
    'start-pj',
    'he-WI',
    'zg-he',
    'pj-fs',
    'start-RW'
]


def add_adjacent_nodes(parsed, node, adjacent_nodes):
    for adj in adjacent_nodes:
        parsed[node].add_adjacent(parsed[adj])


def get_parsed_test_1():
    parsed = {
        'A': Node('A'),
        'b': Node('b'),
        'c': Node('c'),
        'd': Node('d'),
        'end': Node('end'),
        'start': Node('start')
    }
    add_adjacent_nodes(parsed, 'A', ['start', 'c', 'b', 'end'])
    add_adjacent_nodes(parsed, 'b', ['start', 'A', 'd', 'end'])
    add_adjacent_nodes(parsed, 'c', ['A'])
    add_adjacent_nodes(parsed, 'd', ['b'])
    add_adjacent_nodes(parsed, 'end', ['A', 'b'])
    add_adjacent_nodes(parsed, 'start', ['A', 'b'])
    return parsed


def get_parsed_test_2():
    parsed = {
        'dc': Node('dc'),
        'kj': Node('kj'),
        'LN': Node('LN'),
        'HN': Node('HN'),
        'sa': Node('sa'),
        'end': Node('end'),
        'start': Node('start')
    }
    add_adjacent_nodes(parsed, 'dc', ['end', 'start', 'HN', 'LN', 'kj'])
    add_adjacent_nodes(parsed, 'HN', ['start', 'dc', 'end', 'kj'])
    add_adjacent_nodes(parsed, 'kj', ['start', 'sa', 'HN', 'dc'])
    add_adjacent_nodes(parsed, 'LN', ['dc'])
    add_adjacent_nodes(parsed, 'sa', ['kj'])
    add_adjacent_nodes(parsed, 'start', ['dc', 'HN', 'kj'])
    add_adjacent_nodes(parsed, 'end', ['dc', 'HN'])
    return parsed


def get_parsed_test_3():
    parsed = {
        'end': Node('end'),
        'start': Node('start'),
        'fs': Node('fs'),
        'he': Node('he'),
        'DX': Node('DX'),
        'pj': Node('pj'),
        'zg': Node('zg'),
        'sl': Node('sl'),
        'RW': Node('RW'),
        'WI': Node('WI')
    }
    add_adjacent_nodes(parsed, 'fs', ['end', 'he', 'DX', 'pj'])
    add_adjacent_nodes(parsed, 'he', ['fs', 'DX', 'pj', 'RW', 'WI', 'zg'])
    add_adjacent_nodes(parsed, 'DX', ['fs', 'he', 'start', 'pj'])
    add_adjacent_nodes(parsed, 'pj', ['fs', 'he', 'DX', 'start', 'zg', 'RW'])
    add_adjacent_nodes(parsed, 'end', ['fs', 'zg'])
    add_adjacent_nodes(parsed, 'start', ['DX', 'pj', 'RW'])
    add_adjacent_nodes(parsed, 'RW', ['he', 'start', 'zg', 'pj'])
    add_adjacent_nodes(parsed, 'WI', ['he'])
    add_adjacent_nodes(parsed, 'zg', ['he', 'end', 'sl', 'pj', 'RW'])
    add_adjacent_nodes(parsed, 'sl', ['zg'])
    return parsed


def test_parse_input():
    data = parse_input(raw_test_data_1)
    expected = get_parsed_test_1()
    assert data.keys() == expected.keys()
    for k in data.keys():
        assert data[k].symbol == expected[k].symbol
        assert len(data[k].adjacent_nodes) == len(expected[k].adjacent_nodes)
        for s in data[k].adjacent_nodes:
            assert len([a for a in expected[k].adjacent_nodes if a.symbol == s.symbol]) == 1


def test_check_small_caves_only_once():
    assert check_small_caves_only_once(None, Node('test'), deque(['test', 'not']))
    assert not check_small_caves_only_once(None, Node('test'), deque(['foo', 'not']))


def test_check_small_caves_at_most_two():
    # testing 'start' and 'end'
    assert check_small_caves_at_most_two(None, Node('start'), deque(['start', 'not']))
    assert check_small_caves_at_most_two(None, Node('start'), deque(['start', 'start']))
    assert not check_small_caves_at_most_two(None, Node('start'), deque(['test', 'not']))
    # testing other small cave
    nodes = {
        'another': Node('another'),
        'start': Node('start'),
        'not': Node('not'),
        'BIG': Node('BIG')
    }
    assert not check_small_caves_at_most_two(nodes, Node('another'), deque(['start', 'not']))
    assert not check_small_caves_at_most_two(nodes, Node('another'), deque(['another', 'not']))
    assert check_small_caves_at_most_two(nodes, Node('another'), deque(['another', 'another']))
    # testing big cave
    assert not check_small_caves_at_most_two(nodes, Node('BIG'), deque(['start', 'not']))
    assert not check_small_caves_at_most_two(nodes, Node('BIG'), deque(['BIG', 'not']))
    assert not check_small_caves_at_most_two(nodes, Node('BIG'), deque(['BIG', 'BIG']))
    assert not check_small_caves_at_most_two(nodes, Node('BIG'), deque(['BIG', 'BIG', 'BIG']))


@pytest.mark.parametrize("test_data,check_caves_fun,expected",
                         [
                             (get_parsed_test_1(), check_small_caves_only_once, 10),
                             (get_parsed_test_2(), check_small_caves_only_once, 19),
                             (get_parsed_test_3(), check_small_caves_only_once, 226),
                             (get_parsed_test_1(), check_small_caves_at_most_two, 36),
                             (get_parsed_test_2(), check_small_caves_at_most_two, 103),
                             (get_parsed_test_3(), check_small_caves_at_most_two, 3509),
                         ])
def test_find_paths(test_data, check_caves_fun, expected):
    data, _ = find_paths(test_data, check_caves_fun)
    assert data == expected
