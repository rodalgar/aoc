# Day 5: Hydrothermal Venture

from typing import List, Tuple, Dict
import re
import itertools

Point = Tuple[int, int]
Line = Tuple[int, int, int, int]


def parse_input(lines: List[str]) -> List[Line]:
    raw_data = list(map(lambda m: m.groups(),
                        map(re.fullmatch, itertools.repeat(r"^(\d+),(\d+) -> (\d+),(\d+)$"), lines)))
    data = [(int(raw_line[0]), int(raw_line[1]), int(raw_line[2]), int(raw_line[3])) for raw_line in raw_data]
    return data


def is_horizontal(line: Line) -> bool:
    return line[1] == line[3]


def is_vertical(line: Line) -> bool:
    return line[0] == line[2]


def is_ascending_slope(line: Line) -> bool:
    return (line[0] < line[2] and line[1] < line[3]) or (line[0] > line[2] and line[1] > line[3])


def is_descending_slope(line: Line) -> bool:
    return (line[0] < line[2] and line[1] > line[3]) or (line[0] > line[2] and line[1] < line[3])


def sort_lines(lines: List[Line], add_sloped: bool = False) -> List[Line]:
    """
    As segments do not have direction, to make calculations easier we sort each of them from left to right.
    :param lines: list of lines representing the hydrothermal vents
    :param add_sloped: consider sloped lines or not
    :return: sorted lines from left to right
    """
    sorted_lines = []
    for line in lines:
        if is_horizontal(line):
            # from left to right
            if line[0] > line[2]:
                sorted_lines.append((line[2], line[1], line[0], line[3]))
            else:
                sorted_lines.append(line)
        elif is_vertical(line):
            # from top to bottom
            if line[1] > line[3]:
                sorted_lines.append((line[0], line[3], line[2], line[1]))
            else:
                sorted_lines.append(line)
        elif add_sloped and (is_ascending_slope(line) or is_descending_slope(line)):
            if line[0] > line[2]:
                sorted_lines.append((line[2], line[3], line[0], line[1]))
            else:
                sorted_lines.append(line)
        else:
            sorted_lines.append(line)

    return sorted_lines


def expand_lines(lines: List[Line], add_sloped: bool = False) -> List[List[Point]]:
    """
    This method transforms each line into a list of points
    :param lines: list of lines representing the hydrothermal vents
    :param add_sloped: consider sloped lines or not
    :return: List of lists of points
    """
    sorted_lines = sort_lines(lines, add_sloped)
    expanded_lines = []
    for line in sorted_lines:
        if is_horizontal(line):
            expanded_lines.append([(x, line[1]) for x in range(line[0], line[2] + 1)])
        elif is_vertical(line):
            expanded_lines.append([(line[0], y) for y in range(line[1], line[3] + 1)])
        elif add_sloped:
            if is_ascending_slope(line):
                delta = 0
                points = []
                while line[0] + delta <= line[2]:
                    points.append((line[0] + delta, line[1] + delta))
                    delta += 1
                expanded_lines.append(points)
            elif is_descending_slope(line):
                delta = 0
                points = []
                while line[0] + delta <= line[2]:
                    points.append((line[0] + delta, line[1] - delta))
                    delta += 1
                expanded_lines.append(points)

    return expanded_lines


def search_intersections(expanded_lines: List[List[Point]]) -> Dict[str, int]:
    """
    As each line is a set of points, intersections between them is the list of coincident points.
    :param expanded_lines: lines as list of points.
    :return: Dictionary with keys as a representation of a point and value is the number of intersections at the point.
    """
    cross_points = {}
    for i in range(len(expanded_lines)):
        set_line_i = set(expanded_lines[i])
        for j in range(i + 1, len(expanded_lines)):
            set_line_j = set(expanded_lines[j])
            intersections = set_line_i.intersection(set_line_j)
            for intersection in intersections:
                key = f'{intersection[0]}-{intersection[1]}'
                if key not in cross_points:
                    cross_points[key] = 0
                cross_points[key] += 1

    return cross_points


if __name__ == '__main__':
    with open('data/aoc2021-input-day05.txt', 'r') as f:
        sol_raw_lines = [line.strip('\n') for line in f.readlines()]

    sol_lines = parse_input(sol_raw_lines)
    sol_expanded_lines = expand_lines(sol_lines)
    sol_intersections = search_intersections(sol_expanded_lines)
    print('PART 1:')
    print('>>>SOLUTION: ', len(sol_intersections))

    print('PART 2:')
    sol_lines = parse_input(sol_raw_lines)
    sol_expanded_lines = expand_lines(sol_lines, True)
    sol_intersections = search_intersections(sol_expanded_lines)
    print('>>>SOLUTION: ', len(sol_intersections))
