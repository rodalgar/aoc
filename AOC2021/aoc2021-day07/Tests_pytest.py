from Main import parse_input, calculate_fuel_constant, calculate_fuel_accumulating, get_minimum_v6


def get_test_data():
    return [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]


def test_parse_input():
    test_data = "16,1,2,0,4,2,7,1,2,14"
    data = parse_input(test_data)
    assert data == [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]


def test_calculate_fuel_constant():
    data = calculate_fuel_constant(absolute_distance=9)
    assert data == 9


def test_calculate_fuel_accumulating():
    data = calculate_fuel_accumulating(absolute_distance=9)
    assert data == 9 + 8 + 7 + 6 + 5 + 4 + 3 + 2 + 1


def test_get_minimum_part1():
    test_data = get_test_data()
    data = get_minimum_v6(test_data, calculate_fuel_constant)
    assert data == 37


def test_get_minimum_part2():
    test_data = get_test_data()
    data = get_minimum_v6(test_data, calculate_fuel_accumulating)
    assert data == 168
