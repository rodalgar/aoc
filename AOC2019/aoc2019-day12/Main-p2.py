import re
from math import gcd
from functools import reduce


####################################
####################################
# DAY 12, PART 2
####################################
def parse_moon(raw_data):
    """
    Parsing one moon from raw data into a list of coordinates.
    """
    x = re.search('x=(-*[0-9]+)', raw_data).groups(1)[0]
    y = re.search('y=(-*[0-9]+)', raw_data).groups(1)[0]
    z = re.search('z=(-*[0-9]+)', raw_data).groups(1)[0]

    return [int(x), int(y), int(z)]


def lcm(a, b):
    """Perform lcm"""
    return a * b // gcd(a, b)


def get_cycle(moons):
    # Each axis is independent from the others in terms of position and velocity so this means:
    # 1. We can calculate when will each axis repeat itself (at (0, 0, 0) velocity) apart from the others
    # 2. Each axis will repeat itself at a different moment not necessarily the same
    # 3. Solution is the moment in which the three axis repeat themselves at the same time (ie. the LCM of the three)
    initial_positions_per_axis = [[moon[axis] for moon in moons] for axis in range(3)]
    positions_per_axis = [positions_per_axis[:] for positions_per_axis in initial_positions_per_axis]
    velocity_per_axis = [[0 for _ in moons] for _ in range(3)]

    cycles_per_axis = [-1, -1, -1]
    cycle = 0

    while any((cycles_per_axis[axis] == -1 for axis in range(3))):
        cycle += 1

        # for each axis...
        for axis in range(3):
            # if we already know in which cycle, for this axis, a repetition occurs, proceed to the next axis
            if cycles_per_axis[axis] != -1:
                continue
            # first: calculating new velocity
            for i in range(4):
                for j in range(i+1, 4):
                    gravity_pull = (1 if positions_per_axis[axis][i] < positions_per_axis[axis][j]
                                    else -1 if positions_per_axis[axis][i] > positions_per_axis[axis][j]
                                    else 0)
                    velocity_per_axis[axis][i] += gravity_pull
                    velocity_per_axis[axis][j] -= gravity_pull
            # second: updating position with new velocity
            for i in range(4):
                positions_per_axis[axis][i] = positions_per_axis[axis][i] + velocity_per_axis[axis][i]
            # check if this axis is in the original state (position and velocity)
            if initial_positions_per_axis[axis] == positions_per_axis[axis]:
                if velocity_per_axis[axis] == [0, 0, 0, 0]:
                    # OK, this axis repeats itself each 'cycle' iterations
                    cycles_per_axis[axis] = cycle
    return reduce(lcm, cycles_per_axis)


# TEST 1
raw_moons = '<x=-1, y=0, z=2>\n\
<x=2, y=-10, z=-7>\n\
<x=4, y=-8, z=8>\n\
<x=3, y=5, z=-1>'

moon_data_set = [parse_moon(raw_moon) for raw_moon in raw_moons.split('\n')]
repeating_step = get_cycle(moon_data_set)
expected_step = 2772
print('Testing detect_cycle (1)',
      'RIGHT' if expected_step == repeating_step
      else f'WRONG!! Expected {expected_step} but was {repeating_step}')


# TEST 2
raw_moons = '<x=-8, y=-10, z=0>\n\
<x=5, y=5, z=10>\n\
<x=2, y=-7, z=3>\n\
<x=9, y=-8, z=-3>'

moon_data_set = [parse_moon(raw_moon) for raw_moon in raw_moons.split('\n')]
repeating_step = get_cycle(moon_data_set)
expected_step = 4686774924
print('Testing detect_cycle (2)',
      'RIGHT' if expected_step == repeating_step
      else f'WRONG!! Expected {expected_step} but was {repeating_step}')


# SOLUTION
input_12 = r'data\aoc2019-input-day12.txt'
data12 = []
with open(input_12, 'r') as f:
    data12 = [parse_moon(data) for data in f.readlines() if len(data) > 0]

sol_part_2 = get_cycle(data12)
print('SOLUTION PART 2: ', sol_part_2)

