from datetime import datetime
import Moon as m

####################################
####################################
## PART 1
####################################
def tuple_sum(a, b):
    return tuple(p + q for p, q in zip(a, b))


def tuple_dif(a, b):
    return tuple(p - q for p, q in zip(a, b))


def update_moons(moons, num_moons):
    # Calculating gravity pull
    for i in range(num_moons):
        for j in range(i+1, num_moons):
            luna = moons[i]
            other = moons[j]
            gravity = luna.get_gravity_pull(other)
            luna.velocity = tuple_sum(luna.velocity, gravity)
            other.velocity = tuple_dif(other.velocity, gravity)

    # Updating velocity and position
    for moon in moons:
        moon.position = tuple_sum(moon.position, moon.velocity)

    return moons


def update_steps(moons, steps=1, print_each=None):
    print('0 timesteps:')
    for moon in moons:
        moon.print_moon()

    num_moons = len(moons)

    for time_step in range(1, steps+1):
        update_moons(moons, num_moons)
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

#TEST 1
print('TEST 1')
raw_moons = '<x=-1, y=0, z=2>\n\
<x=2, y=-10, z=-7>\n\
<x=4, y=-8, z=8>\n\
<x=3, y=5, z=-1>'

moons = [m.Moon.parse_moon(str(i), raw_moon) for i, raw_moon in enumerate(raw_moons.split('\n'))]

moons = update_steps(moons, 10, 1)
print('Energía total', get_system_energy(moons))

#TEST 2
print('TEST 2')
raw_moons = '<x=-8, y=-10, z=0>\n\
<x=5, y=5, z=10>\n\
<x=2, y=-7, z=3>\n\
<x=9, y=-8, z=-3>'

moons = [m.Moon.parse_moon(str(i), raw_moon) for i, raw_moon in enumerate(raw_moons.split('\n'))]

moons = update_steps(moons, 100, 10)
print('Energía total', get_system_energy(moons))


# SOLUTION PART 1
input_12 = r'data\aoc2019-input-day12.txt'
data12=[]
with open(input_12, 'r') as f:
    data12 = [m.Moon.parse_moon(str(number), data) for number, data in enumerate(f.readlines()) if len(data) > 0]

moons = update_steps(data12, 1000, 1000)
print('Energía total', get_system_energy(moons))

#>>>SOLUTION: 7077

exit(0)

####################################
####################################
## PART 2
####################################

#TEST 1
raw_moons = '<x=-1, y=0, z=2>\n\
<x=2, y=-10, z=-7>\n\
<x=4, y=-8, z=8>\n\
<x=3, y=5, z=-1>'

moons = [m.Moon.parse_moon(str(i), rawmoon) for i, rawmoon in enumerate(raw_moons.split('\n'))]

#TEST 2
raw_moons = '<x=-8, y=-10, z=0>\n\
<x=5, y=5, z=10>\n\
<x=2, y=-7, z=3>\n\
<x=9, y=-8, z=-3>'

moons = [m.Moon.parse_moon(str(i), rawmoon) for i, rawmoon in enumerate(raw_moons.split('\n'))]


exit(0)

#SOLUTION
input_12 = r'data\aoc2019-input-day12.txt'
data12=[]
with open(input_12, 'r') as f:
    data12 = [m.Moon.parse_moon(str(number), data) for number, data in enumerate(f.readlines()) if len(data) > 0]

# print(f'| {datetime.now()} | Empezamossss')
# isFound, step = getRepeatedStatus(data12)
# print(f'| {datetime.now()} | Terminamossss')

