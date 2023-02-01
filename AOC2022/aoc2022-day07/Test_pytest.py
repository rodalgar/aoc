import pytest

from Main import parse_input, eval_files_p1, FS_ENTRY_TYPE_FILE, FS_ENTRY_TYPE_DIR, eval_files_p2, get_dirs_recur, solve_p2

test_raw_data = [
    '$ cd /',
    '$ ls',
    'dir a',
    '14848514 b.txt',
    '8504156 c.dat',
    'dir d',
    '$ cd a',
    '$ ls',
    'dir e',
    '29116 f',
    '2557 g',
    '62596 h.lst',
    '$ cd e',
    '$ ls',
    '584 i',
    '$ cd ..',
    '$ cd ..',
    '$ cd d',
    '$ ls',
    '4060174 j',
    '8033020 d.log',
    '5626152 d.ext',
    '7214296 k'
]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data[2] == 48381165
    assert len(data[4]) == 4
    assert 'a' in data[4]
    assert 'b.txt' in data[4]
    assert 'c.dat' in data[4]
    assert 'd' in data[4]
    assert len(data[4]['a'][4]) == 4
    assert 'e' in data[4]['a'][4]
    assert 'f' in data[4]['a'][4]
    assert 'g' in data[4]['a'][4]
    assert 'h.lst' in data[4]['a'][4]


@pytest.mark.parametrize("test_data, expected", [
    (['blabla', FS_ENTRY_TYPE_FILE, 5000, None, None], False),
    (['blabla', FS_ENTRY_TYPE_FILE, 150000, None, None], False),
    (['blabla', FS_ENTRY_TYPE_DIR, 5000, None, None], True),
    (['blabla', FS_ENTRY_TYPE_DIR, 150000, None, None], False),
])
def test_eval_files_p1(test_data, expected):
    data = eval_files_p1(test_data)
    assert data == expected


@pytest.mark.parametrize("test_data, expected", [
    (['blabla', FS_ENTRY_TYPE_FILE, 5000, None, None], False),
    (['blabla', FS_ENTRY_TYPE_FILE, 150000, None, None], False),
    (['blabla', FS_ENTRY_TYPE_DIR, 5000, None, None], False),
    (['blabla', FS_ENTRY_TYPE_DIR, 150000, None, None], True),
])
def test_eval_files_p2(test_data, expected):
    data = eval_files_p2(test_data, 10000)
    assert data == expected


def mock_eval_fun(line):
    assert line[1] == FS_ENTRY_TYPE_DIR, f'Only directories should be evaluated!'
    return line[0] in ['a', 'd', 'e']


def test_get_dirs_recur():
    data = get_dirs_recur(parse_input(test_raw_data), mock_eval_fun)
    assert len(data) == 3
    for d in data:
        assert d[0] in ['a', 'd', 'e']


def test_solve_p2():
    data = solve_p2(parse_input(test_raw_data), 70000000, 30000000)
    assert data == 24933642
