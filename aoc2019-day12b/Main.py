import re
import numpy as np
from datetime import datetime

'''
Plain version without classes.
'''

def parseMoon(rawline):
    # RawData sample:
    # <x=-1, y=7, z=3>
    x = re.search('x=(-*[0-9]+)', rawline).groups(1)[0]
    # print('x vale', x)
    y = re.search('y=(-*[0-9]+)', rawline).groups(1)[0]
    # print('y vale', y)
    z = re.search('z=(-*[0-9]+)', rawline).groups(1)[0]
    # print('z vale', z)

    # return Moon(label, np.array([int(x), int(y), int(z)], dtype=int))
    return int(x), int(y), int(z)

def parseMoons(rawdata):
    moons = [parseMoon(rawmoon) for rawmoon in rawdata.split('\n')]

    lx = []
    ly = []
    lz = []

    for sublist in moons:
        lx.append(sublist[0])
        ly.append(sublist[1])
        lz.append(sublist[2])

    x = np.array(lx, dtype=int)
    y = np.array(ly, dtype=int)
    z = np.array(lz, dtype=int)

    vx = np.zeros(4, dtype=int)
    vy = np.zeros(4, dtype=int)
    vz = np.zeros(4, dtype=int)

    return x, y, z, vx, vy, vz

def getdpos(vec):
    return np.array([vec, np.concatenate([vec[1:], vec[:1]]), np.concatenate([vec[2:], vec[:2]]), np.concatenate([vec[3:], vec[:3]])], dtype=int)
    # return np.array([vec, np.roll(vec, 1), np.roll(vec, 2), np.roll(vec, 3)])

def getgravpull(pos, dpos):
    return np.sum(np.sign(dpos - pos), axis=0)

def getepot(posx, posy, posz):
    return np.abs(posx) + np.abs(posy) + np.abs(posz)

def getekin(velx, vely, velz):
    return np.abs(velx) + np.abs(vely) + np.abs(velz)

def getetotal(epot, ekin):
    return np.sum(epot * ekin)

def updateMoons(moons, steps = 1):
    (x, y, z, vx, vy, vz) = moons

    for i in range(steps):
        # dx = np.array([x, np.concatenate([x[1:], x[:1]]), np.concatenate([x[2:], x[:2]]), np.concatenate([x[3:], x[:3]])], dtype=int)
        # dy = np.array([y, np.concatenate([y[1:], y[:1]]), np.concatenate([y[2:], y[:2]]), np.concatenate([y[3:], y[:3]])], dtype=int)
        # dz = np.array([z, np.concatenate([z[1:], z[:1]]), np.concatenate([z[2:], z[:2]]), np.concatenate([z[3:], z[:3]])], dtype=int)
        dx = getdpos(x)
        dy = getdpos(y)
        dz = getdpos(z)

        #calculamos fuerza gravitatoria
        # gx = np.sum(np.sign(dx - x), axis=0)
        # gy = np.sum(np.sign(dy - y), axis=0)
        # gz = np.sum(np.sign(dz - z), axis=0)
        gx = getgravpull(x, dx)
        gy = getgravpull(y, dy)
        gz = getgravpull(z, dz)

        # actualizamos la velocidad
        vx += gx
        vy += gy
        vz += gz

        # recalculamos la posición
        x += vx
        y += vy
        z += vz

        # cálculo de las energías...
        # epot = np.abs(x) + np.abs(y) + np.abs(z)
        # ekin = np.abs(vx) + np.abs(vy) + np.abs(vz)
        # etot = np.sum(epot * ekin)
        epot = getepot(x, y, z)
        ekin = getekin(vx, vy, vz)
        etot = getetotal(epot, ekin)

    return x, y, z, vx, vy, vz, epot, ekin, etot

def solveProblem(rawMoons, steps = 1):
    moons = parseMoons(rawMoons)

    print(moons)
    print(f'| {datetime.now()} | Start solving.')
    moons = updateMoons(moons, steps)
    print(f'| {datetime.now()} | End solving.')
    print(moons)

#TEST 1:
print('TEST 1')
rawMoons = '<x=-1, y=0, z=2>\n\
<x=2, y=-10, z=-7>\n\
<x=4, y=-8, z=8>\n\
<x=3, y=5, z=-1>'

solveProblem(rawMoons, 10)

#TEST 2:
print('TEST 2')
rawMoons = '<x=-8, y=-10, z=0>\n\
<x=5, y=5, z=10>\n\
<x=2, y=-7, z=3>\n\
<x=9, y=-8, z=-3>'

solveProblem(rawMoons, 100)

#SOLUTION
print('SOLUTION PART 1')
input_12 = r'data\aoc2019-input-day12.txt'
data12=[]
with open(input_12, 'r') as f:
    #data12 = [m.Moon.parseMoon(str(number), data) for number, data in enumerate(f.readlines()) if len(data) > 0]
    data12 = f.read()

# import yappi
#
# yappi.set_clock_type("wall")
# yappi.start(builtins=True)

solveProblem(data12, 2000000)

# yappi.get_func_stats().print_all()
# yappi.get_thread_stats().print_all()
# callgrind_filename = f'callgrind.filename.{datetime.now().strftime("%Y%m%d_%H%M%S")}.prof'
# stats = yappi.get_func_stats()
# stats.save(rf'C:\Users\rodrigo\PyCharmProjects\aoc2019-day12b\{callgrind_filename}', type='callgrind')
