# Day 13: Transparent Origami
import copy
from typing import List, Tuple


def parse_input(raw_instructions: List[str]) -> Tuple[List[List[int]], List[Tuple[str, int]]]:
    reading_coordinates = True
    points = []
    folding = []
    for instruction in raw_instructions:
        if reading_coordinates:
            if len(instruction) > 0:
                x, y = instruction.split(',')
                points.append([int(x), int(y)])
            else:
                reading_coordinates = False
        else:
            _, _, fold_data = instruction.split(' ')
            fold_direction, fold_coordinate = fold_data.split('=')
            folding.append((fold_direction, int(fold_coordinate)))
    return points, folding


def print_paper(points: List[List[int]]) -> List[str]:
    printed_paper = []
    max_x, max_y = 0, 0
    for point in points:
        if point[0] > max_x:
            max_x = point[0]
        if point[1] > max_y:
            max_y = point[1]

    for row in range(max_y + 1):
        col = ['.'] * (max_x + 1)
        for p in (p for p in points if p[1] == row):
            col[p[0]] = '#'
        printed_paper.append(''.join(col))

    return printed_paper



def fold_paper(points_in: List[List[int]], fold_data: Tuple[str, int]) -> List[List[int]]:
    points = copy.deepcopy(points_in)
    if fold_data[0] == 'x':
        # horizontal fold to the left
        points_to_change = [p for p in points if p[0] > fold_data[1]]
        for point in points_to_change:
            delta_x = point[0] - fold_data[1]
            new_x = fold_data[1] - delta_x
            if [new_x, point[1]] in points:
                # print(f'point was {point[0]}, {point[1]} now is {new_x},{point[1]} but already exists')
                points.remove(point)
            else:
                point[0] = new_x
        pass
    elif fold_data[0] == 'y':
        # Vertical fold upwards
        points_to_change = [p for p in points if p[1] > fold_data[1]]
        for point in points_to_change:
            delta_y = point[1] - fold_data[1]
            new_y = fold_data[1] - delta_y
            if [point[0], new_y] in points:
                # print(f'point was {point[0]}, {point[1]} now is {point[0]},{new_y} but already exists')
                points.remove(point)
            else:
                point[1] = new_y
    else:
        raise Exception(f'Unknown folding direction! ({fold_data})')

    return points


if __name__ == '__main__':
    with open('data/aoc2021-input-day13.txt', 'r') as f:
        sol_raw_instructions = [line.strip('\n') for line in f.readlines()]

    # PART 1
    sol_points, sol_foldings = parse_input(sol_raw_instructions)
    sol_points_2 = fold_paper(sol_points, sol_foldings[0])
    print('PART 1')
    print('>>>SOLUTION:', len(sol_points_2))

    # PART 2
    for folding_data in sol_foldings:
        sol_points = fold_paper(sol_points, folding_data)

    print('PART 2')
    print_paper(sol_points)
    print('>>>SOLUTION: RLBCJGLU')
