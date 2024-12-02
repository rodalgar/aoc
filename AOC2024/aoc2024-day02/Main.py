# Day 2: Red-Nosed Reports
import operator
from typing import Optional


def parse_input(raw_data: [str]) -> [[int]]:
    return [list(map(int, report.split())) for report in raw_data]


def analyze_report(report: [int]) -> (bool, Optional[int], str):
    # Case base is undefined, although every logic is applied to sets of numbers of length equal or greater than 2
    if len(report) < 2:
        return False, None, f'report too short (length {len(report)})'
    cmp_operator = None

    for ix in range(1, len(report)):
        delta = report[ix] - report[ix - 1]
        # First pair does not know yet if the array is increasing or decreasing, so we figure it out here.
        if cmp_operator is None:
            if delta > 0:
                cmp_operator = operator.gt
            elif delta < 0:
                cmp_operator = operator.lt
            else:
                return False, ix, f'initially monotonic report {report[ix]} and {report[ix - 1]}'
        # pre-condition monotonic series is unsafe
        if report[ix] == report[ix - 1]:
            return False, ix, f'monotonic report {report[ix]} and {report[ix - 1]}'
        # condition 1: Distance must be 3 or less
        if abs(delta) > 3:
            return False, ix, f'distance greater than 3 (data was {report[ix - 1]} then {report[ix]} diff {delta})'
        # must observe agreed growth behaviour
        if not cmp_operator(report[ix], report[ix - 1]):
            return False, ix, (f'change of growth behaviour (was {cmp_operator.__name__} but data was {report[ix - 1]} '
                               f'then {report[ix]}')
    return True, None


def analyze_all(raw_reports, use_problem_dampener=False, verbose=False):
    if verbose:
        print('Analyzing', len(raw_reports))
    safe_reports = 0
    for report in raw_reports:
        str_analysis = f'analyzing {report}'
        result = analyze_report(report)
        if result[0]:
            str_analysis += ' OK'
            safe_reports += 1
        else:
            str_analysis += f' ERR {result}'
            if use_problem_dampener:
                # Let's try to fix the report removing a level at a time from the position where
                # the error was found. We need to go back 2 positions because in cases of changing growth
                # behaviour you need 3 points to discover the problem. Not always is needed to go
                # back 2 positions, other errors might require only one, but this is better than
                # start chopping heads from the beginning of the report.
                initial_err_position = max(0, result[1] - 2)
                for err_position in range(initial_err_position, len(report)):
                    new_report = report[:err_position] + report[err_position + 1:]
                    str_analysis += f'Trying {new_report}'
                    new_result = analyze_report(new_report)
                    if new_result[0]:
                        str_analysis += f'. Using PD: {new_report} was safe'
                        safe_reports += 1
                        break
                    else:
                        str_analysis += ' NOT GOOD.'
            if verbose:
                print(str_analysis)
    return safe_reports


if __name__ == '__main__':
    with open('data/aoc2024-input-day02.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_data = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', analyze_all(sol_data))

    print('PART 2')
    print('>>>>SOLUTION: ', analyze_all(sol_data, use_problem_dampener=True))
