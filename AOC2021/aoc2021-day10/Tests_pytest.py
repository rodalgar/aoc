from collections import deque
import pytest

from Main import ValidationResult, check_line, process_lines, calculate_syntax_error_score, evaluate_incomplete, \
    get_best_incomplete_score

test_raw_data = [
    '[({(<(())[]>[[{[]{<()<>>',
    '[(()[<>])]({[<{<<[]>>(',
    '{([(<{}[<>[]}>{[]{[(<()>',
    '(((({<>}<{<{<>}{[]{[]{}',
    '[[<[([]))<([[{}[[()]]]',
    '[{[{({}]{}}([{[{{{}}([]',
    '{<[[]]>}<{[{[{[]{()[[[]',
    '[<(<(<(<{}))><([]([]()',
    '<{([([[(<>()){}]>(<<{{',
    '<{([{{}}[<[[[<>{}]]]>[]]'
]


@pytest.mark.parametrize("test_data,expected",
                         [
                             # OK
                             ('()', (ValidationResult.OK, None, 0)),
                             ('[]', (ValidationResult.OK, None, 0)),
                             ('([])', (ValidationResult.OK, None, 0)),
                             ('{()()()}', (ValidationResult.OK, None, 0)),
                             ('<([{}])>', (ValidationResult.OK, None, 0)),
                             ('[<>({}){}[([])<>]]', (ValidationResult.OK, None, 0)),
                             ('(((((((((())))))))))', (ValidationResult.OK, None, 0)),
                             # CORRUPTED
                             ('(]', (ValidationResult.CORRUPTED, 1, 57)),
                             ('{()()()>', (ValidationResult.CORRUPTED, 7, 25137)),
                             ('(((()))}', (ValidationResult.CORRUPTED, 7, 1197)),
                             ('<([]){()}[{}])', (ValidationResult.CORRUPTED, 13, 3))
                         ])
def test_check_line(test_data, expected):
    data = check_line(test_data)
    assert data == expected


def test_process_lines():
    data = process_lines(test_raw_data)
    assert data == [(ValidationResult.INCOMPLETE, deque([']', ')', '}', ')', ']', ']', '}', '}']), 0),
                    (ValidationResult.INCOMPLETE, deque([')', '}', ']', '>', '}', ')']), 0),
                    (ValidationResult.CORRUPTED, 12, 1197),
                    (ValidationResult.INCOMPLETE, deque([')', ')', ')', ')', '>', '}', '>', '}', '}']), 0),
                    (ValidationResult.CORRUPTED, 8, 3), (ValidationResult.CORRUPTED, 7, 57),
                    (ValidationResult.INCOMPLETE, deque(['>', '}', ']', '}', ']', '}', '}', ']', ']']), 0),
                    (ValidationResult.CORRUPTED, 10, 3), (ValidationResult.CORRUPTED, 16, 25137),
                    (ValidationResult.INCOMPLETE, deque(['>', '}', ')', ']']), 0)]


def test_calculate_syntax_error_score():
    data = calculate_syntax_error_score(test_raw_data)
    assert data == 26397


def test_evaluate_incomplete():
    data = evaluate_incomplete((ValidationResult.INCOMPLETE, deque([']', ')', '}', ')', ']', ']', '}', '}']), 0))
    assert data == 288957


def test_get_best_incomplete_score():
    data = get_best_incomplete_score(test_raw_data)
    assert data == 288957
