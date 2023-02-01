import pytest

from Main import get_visible_trees, get_scenic_score, get_best_scenic_score

test_raw_data = [
    '30373',
    '25512',
    '65332',
    '33549',
    '35390'
]


def test_get_visible_trees():
    data = get_visible_trees(test_raw_data)
    assert data == {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 4), (2, 0), (2, 1),
                    (2, 3), (2, 4), (3, 0), (3, 2), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)}


@pytest.mark.parametrize("row, column, expected", [
    (1, 2, 4),
    (3, 2, 8),
])
def test_get_scenic_score(row, column, expected):
    data = get_scenic_score(test_raw_data, row, column)
    assert data == expected


def test_get_best_scenic_score():
    data = get_best_scenic_score(test_raw_data)
    assert data[0] == 8
    assert data[1] == (3, 2)
