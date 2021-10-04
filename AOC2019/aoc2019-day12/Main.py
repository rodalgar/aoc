import numpy as np
from Moon import Moon
from functools import reduce
from math import gcd
import operator


####################################
####################################
# PART 1
####################################
def update_moons(moons):
    num_moons = len(moons)

    # Calculating gravity pull. This is a symmetric relationship
    for i in range(num_moons):
        for j in range(i+1, num_moons):
            luna = moons[i]
            other = moons[j]
            luna.get_gravity_pull(other)

    # Updating velocity and position
    for moon in moons:
        moon.position = [a+b for a, b in zip(moon.position, moon.velocity)]

    return moons


def update_steps(moons, *, steps=1, print_each=None, verbose=False):
    if verbose:
        print('0 time steps:')
        for moon in moons:
            moon.print_moon()

    for time_step in range(1, steps+1):
        update_moons(moons)
        if print_each is not None and time_step % print_each == 0:
            print('Step', time_step)
            for moon in moons:
                moon.print_moon()

    return moons


def get_system_energy(moons):
    total = 0
    for moon in moons:
        total += moon.get_total_energy()
    return total


# TEST 1
print('TEST 1')
raw_moons = '<x=-1, y=0, z=2>\n\
<x=2, y=-10, z=-7>\n\
<x=4, y=-8, z=8>\n\
<x=3, y=5, z=-1>'

moon_data_set = [Moon.parse_moon(str(i), raw_moon) for i, raw_moon in enumerate(raw_moons.split('\n'))]
moon_data_set = update_steps(moon_data_set, steps=10)

test_energy = get_system_energy(moon_data_set)
expected_energy = 179
print('Testing get_system_energy (1)',
      'RIGHT' if expected_energy == test_energy
      else f'WRONG!! Expected {expected_energy} but was {test_energy}')


# TEST 2
print('TEST 2')
raw_moons = '<x=-8, y=-10, z=0>\n\
<x=5, y=5, z=10>\n\
<x=2, y=-7, z=3>\n\
<x=9, y=-8, z=-3>'

moon_data_set = [Moon.parse_moon(str(i), raw_moon) for i, raw_moon in enumerate(raw_moons.split('\n'))]
moon_data_set = update_steps(moon_data_set, steps=100)

test_energy = get_system_energy(moon_data_set)
expected_energy = 1940
print('Testing get_system_energy (2)',
      'RIGHT' if expected_energy == test_energy
      else f'WRONG!! Expected {expected_energy} but was {test_energy}')

# SOLUTION PART 1
input_12 = r'data\aoc2019-input-day12.txt'
data12 = []
with open(input_12, 'r') as f:
    data12 = [Moon.parse_moon(str(number), data) for number, data in enumerate(f.readlines()) if len(data) > 0]

moon_data_set = update_steps(data12, steps=1000, print_each=1000)
print('Total energy', get_system_energy(moon_data_set))

# >>>SOLUTION: 7077
