from Main import parse_input, part1, part2, Point, Data

test_raw_data = [
    'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
    'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
    'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
    'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
    'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
    'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
    'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
    'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
    'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
    'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
    'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
    'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
    'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
    'Sensor at x=20, y=1: closest beacon is at x=15, y=3'
]


def get_test_data():
    return [Data(sensor=Point(x=2, y=18), beacon=Point(x=-2, y=15)),
            Data(sensor=Point(x=9, y=16), beacon=Point(x=10, y=16)),
            Data(sensor=Point(x=13, y=2), beacon=Point(x=15, y=3)),
            Data(sensor=Point(x=12, y=14), beacon=Point(x=10, y=16)),
            Data(sensor=Point(x=10, y=20), beacon=Point(x=10, y=16)),
            Data(sensor=Point(x=14, y=17), beacon=Point(x=10, y=16)),
            Data(sensor=Point(x=8, y=7), beacon=Point(x=2, y=10)),
            Data(sensor=Point(x=2, y=0), beacon=Point(x=2, y=10)),
            Data(sensor=Point(x=0, y=11), beacon=Point(x=2, y=10)),
            Data(sensor=Point(x=20, y=14), beacon=Point(x=25, y=17)),
            Data(sensor=Point(x=17, y=20), beacon=Point(x=21, y=22)),
            Data(sensor=Point(x=16, y=7), beacon=Point(x=15, y=3)),
            Data(sensor=Point(x=14, y=3), beacon=Point(x=15, y=3)),
            Data(sensor=Point(x=20, y=1), beacon=Point(x=15, y=3))]


def test_parse_input():
    data = parse_input(test_raw_data)
    assert data == get_test_data()


def test_part1():
    data, _ = part1(get_test_data(), 10)
    assert data == 26


def test_part2():
    data, row, col, _ = part2(get_test_data(), (0, 20))
    assert row == 11
    assert col == 14
    assert data == 56000011
