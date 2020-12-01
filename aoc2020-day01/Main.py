# DAY 1: Day 1: Report Repair
# PART 1


# function
def get_values_two(vals, target_sum):
    int_data = [int(x) for x in vals]
    int_data.sort()

    for x in range(len(vals)):
        for y in range(x+1, len(vals)):
            suma = int_data[x] + int_data[y]
            if suma == target_sum:
                return int_data[x], int_data[y], suma, int_data[x] * int_data[y]
            elif suma > target_sum:
                break

    return None


# Test
def test_part_1(test_values, target):
    (a, b, sum_ab, prod_ab) = get_values_two(test_values, target)

    print('example 1', 'RIGHT' if sum_ab == target else 'WRONG', a, b, sum_ab, prod_ab)


# Solution
def solve_part_1(data, target):
    solution = get_values_two(data, target)
    print(solution)


# PART 2
def get_values_three(vals, target_sum):
    int_data = [int(x) for x in vals]
    int_data.sort()

    for x in range(len(vals)):
        for y in range(x+1, len(vals)):
            for z in range(y+1, len(vals)):
                suma = int_data[x] + int_data[y] + int_data[z]
                if suma == target_sum:
                    return int_data[x], int_data[y], int_data[z], suma, int_data[x] * int_data[y] * int_data[z]
                elif suma > target_sum:
                    continue

    return None


# Test
def test_part_2(test_values, target):
    (a, b, c, sum_abc, prod_abc) = get_values_three(test_values, target)

    print('example 2', 'RIGHT' if sum_abc == target else 'WRONG', a, b, c, sum_abc, prod_abc)


# Solution
def solve_part_2(data, target):
    sol = get_values_three(data, target)
    print(sol)


if __name__ == '__main__':
    test_values = ['1721', '979', '366', '299', '675', '1456']
    target = 2020
    with open('data/aoc2020-input-day01.txt', 'r') as f:
        problem_data = [line for line in f.readlines()]

    # PART 1
    # TEST
    test_part_1(test_values, target)

    # SOLVE
    print('SOLVING 1')
    solve_part_1(problem_data, target)
    print()

    # PART 2
    # TEST
    test_part_2(test_values, target)

    #SOLVE
    print('SOLVING 2')
    solve_part_2(problem_data, target)
