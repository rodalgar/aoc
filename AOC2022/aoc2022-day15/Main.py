# Day 15: Beacon Exclusion Zone
import operator
import re
from collections import namedtuple
from functools import reduce

Point = namedtuple("Point", "x y")
Data = namedtuple("Data", "sensor beacon ")


def manhattan_distance(point_a, point_b):
    return abs(point_a.x - point_b.x) + abs(point_a.y - point_b.y)


def parse_input(raw):
    regexp = r'[^=]+=(-*\d+), y=(-*\d+):[^=]+=(-*\d+), y=(-*\d+)'
    observations = []
    for line in raw:
        coordinates = re.findall(regexp, line)[0]
        observation = Data(sensor=Point(int(coordinates[0]), int(coordinates[1])),
                           beacon=Point(int(coordinates[2]), int(coordinates[3])))
        observations.append(observation)
    return observations


def part1(observations, y_reference, verbose=False):
    def range_overlap(range_a, range_b):
        left_range = range_a if range_a.start < range_b.start else range_b
        right_range = range_b if left_range == range_a else range_a
        return left_range.stop >= right_range.start

    def merge_ranges(ranges):
        ranges_copy = ranges.copy()
        merged = [ranges_copy[0]]
        del ranges_copy[0]

        restart = False
        while True:
            merged_one = False
            for i in range(len(ranges_copy)):
                if restart:
                    restart = False
                    break
                for j in range(len(merged)):
                    if range_overlap(ranges_copy[i], merged[j]):
                        new_range = range(min(ranges_copy[i].start, merged[j].start),
                                          max(ranges_copy[i].stop, merged[j].stop))
                        merged.append(new_range)
                        del merged[j]
                        del ranges_copy[i]
                        restart = True
                        merged_one = True
                        break
                if not merged_one:
                    merged.append(ranges_copy[i])
            if not merged_one:
                break
        return merged

    y_sensor_projections = []
    for o in observations:
        distance = manhattan_distance(o.sensor, o.beacon)
        sensor_y_distance = abs(o.sensor.y - y_reference)
        if sensor_y_distance <= distance:
            x_offset = distance - sensor_y_distance
            y_sensor_projections.append(range(o.sensor.x - x_offset, o.sensor.x + x_offset + 1))
    if verbose:
        print(y_sensor_projections)
    y_sensor_projections.sort(key=lambda a: a.stop)
    y_sensor_projections.sort(key=lambda a: a.start)
    if verbose:
        print(y_sensor_projections)

    projection = merge_ranges(y_sensor_projections)
    if verbose:
        print('>', projection)

    # remove sensors on projection
    sensors_on_projection = len([observation for observation in observations if observation.sensor.y == y_reference])

    unoccupied_tiles = reduce(operator.add, map(len, projection)) - len(projection) - sensors_on_projection
    return unoccupied_tiles, projection


def part2(observations, clip_ranges_to, verbose=False):
    min_range, max_range = clip_ranges_to

    for y_ref in range(min_range, max_range + 1):
        if verbose:
            print('y_ref', y_ref)
        result = part1(observations, y_ref, verbose=verbose)
        if verbose:
            print(result)
        if len(result[1]) > 1:
            row = y_ref
            col = result[1][0].stop
            frequency = col * 4000000 + row
            return frequency, row, col, result
    return None


if __name__ == '__main__':
    with open('data/aoc2022-input-day15.txt', 'r') as f:
        raw_data = [line.strip('\n') for line in f.readlines()]

    data = parse_input(raw_data)

    print('PART 1')
    print('>>>SOLUTION: ', part1(data, 2000000))

    print('PART 2')
    print('>>>SOLUTION: ', part2(data, (0, 4000000)))
