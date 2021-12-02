# PART 1
from Main import parse_path, resolve_path_from, resolve_path_from_v2

raw_path = ['forward 5',
            'down 5',
            'forward 8',
            'up 3',
            'down 8',
            'forward 2'
            ]


def test_parse_path():
    data = parse_path(raw_path)

    assert data == [((1, 0), 5), ((0, 1), 5), ((1, 0), 8), ((0, -1), 3), ((0, 1), 8), ((1, 0), 2)]


def test_resolve_path_from():
    instructions = [((1, 0), 5), ((0, 1), 5), ((1, 0), 8), ((0, -1), 3), ((0, 1), 8), ((1, 0), 2)]
    origin = (0, 0)
    data = resolve_path_from(instructions, origin)

    assert data == (15, 10)


def test_resolve_path_from_v2():
    instructions = [((1, 0), 5), ((0, 1), 5), ((1, 0), 8), ((0, -1), 3), ((0, 1), 8), ((1, 0), 2)]
    origin = (0, 0, 0)
    data = resolve_path_from_v2(instructions, origin)

    assert data == (15, 60)
