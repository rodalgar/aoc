#import numpy as np
import shelve
from datetime import datetime
import Moon as m

'''
First version.
'''


####################################
####################################
## PART 1
####################################
def tuple_sum(a, b):
    return tuple(p + q for p, q in zip(a, b))

def tuple_dif(a, b):
    return tuple(p - q for p, q in zip(a, b))

def updateMoons(moons, num_moons):
    # Calculating gravity pull
    for i in range(num_moons):
        for j in range(i+1, num_moons):
            # if i != j:
            luna = moons[i]
            other = moons[j]
            gravluna = luna.getGravityPull(other)
            # luna.velocity += gravluna
            # other.velocity -= gravluna
            luna.velocity = tuple_sum(luna.velocity, gravluna)
            other.velocity = tuple_dif(other.velocity, gravluna)


    # Updating velocity and position
    for moon in moons:
        # moon.position += moon.velocity
        moon.position = tuple_sum(moon.position, moon.velocity)

    return moons

def updateSteps(moons, steps=1, printEach=None):
    print('0 timesteps:')
    for moon in moons:
        moon.printMoon()

    num_moons = len(moons)

    for step in range(1, steps+1):
        updateMoons(moons, num_moons)
        if printEach is not None and step % printEach == 0:
            print('Step', step)
            for moon in moons:
                moon.printMoon()

    return moons

def getSystemEnergy(moons):
    total = 0
    for moon in moons:
        total += moon.getTotalEnergy()
    return total

#TEST 1
print('TEST 1')
rawMoons = '<x=-1, y=0, z=2>\n\
<x=2, y=-10, z=-7>\n\
<x=4, y=-8, z=8>\n\
<x=3, y=5, z=-1>'

moons = [m.Moon.parseMoon(str(i), rawmoon) for i, rawmoon in enumerate(rawMoons.split('\n'))]

moons = updateSteps(moons, 10, 1)
print('Energía total', getSystemEnergy(moons))

#TEST 2
print('TEST 2')
rawMoons = '<x=-8, y=-10, z=0>\n\
<x=5, y=5, z=10>\n\
<x=2, y=-7, z=3>\n\
<x=9, y=-8, z=-3>'

moons = [m.Moon.parseMoon(str(i), rawmoon) for i, rawmoon in enumerate(rawMoons.split('\n'))]

moons = updateSteps(moons, 100, 10)
print('Energía total', getSystemEnergy(moons))


# SOLUTION PART 1
input_12 = r'data\aoc2019-input-day12.txt'
data12=[]
with open(input_12, 'r') as f:
    data12 = [m.Moon.parseMoon(str(number), data) for number, data in enumerate(f.readlines()) if len(data) > 0]

moons = updateSteps(data12, 1000, 1000)
print('Energía total', getSystemEnergy(moons))

#>>>SOLUTION: 7077

####################################
####################################
## PART 2
####################################

def getVectorHash(vecHash, vec, next_hash_value):
    # theKey = vec.data.tobytes()
    theKey = str(vec)
    # theKey = hash(vec.tostring())
    # theKey = hash(str(vec))
    existed = True
    # if theKey not in vecHash:
    valor = vecHash.get(theKey)
    if valor is None:
        existed = False
        next_hash_value += 1
        vecHash[theKey] = next_hash_value
        return next_hash_value, existed, next_hash_value
    return valor, existed, next_hash_value


# def hashMoon(vecHash, moon, next_vec_hash_value):
#     hashPos, _, next_vec_hash_value = getVectorHash(vecHash, moon.position, next_vec_hash_value)
#     hashVel, _, next_vec_hash_value = getVectorHash(vecHash, moon.velocity, next_vec_hash_value)
#     return hashPos, hashVel, next_vec_hash_value

def hashSystem(sysHash, vecHash, moons, num_moons, next_sys_hash_value ,next_vec_hash_value):
    # systemStatus = np.zeros((num_moons, 2))
    systemStatus = []

    # for i in range(num_moons):
    #     m = moons[i]
    #     hashPos, hashVel, next_vec_hash_value = hashMoon(vecHash, m, next_vec_hash_value)
        # systemStatus[i, 0] = hashPos
        # systemStatus[i, 1] = hashVel
        # systemStatus.append(hashPos)
        # systemStatus.append(hashVel)

    # can_cache_status = True
    # for i in range(num_moons):
    #     if not can_cache_status:
    #         break
    #     for j in range(i+1, num_moons):
    #         dis = tuple_dif(moons[i].position, moons[j].position)
    #         if max(tuple(abs(d) for d in dis)) > 70:
    #             can_cache_status = False
    #             # print(moons[i].position, moons[j].position, dis, max(tuple(abs(d) for d in dis)), '\n-----')
    #             break
    total_kinetic = sum([m.getKineticEnergy() for m in moons])
    can_cache_status = total_kinetic == 0

    existed = False
    if can_cache_status:
        hashPos0, _, next_vec_hash_value = getVectorHash(vecHash, moons[0].position, next_vec_hash_value)
        hashVel0, _, next_vec_hash_value = getVectorHash(vecHash, moons[0].velocity, next_vec_hash_value)
        hashPos1, _, next_vec_hash_value = getVectorHash(vecHash, moons[1].position, next_vec_hash_value)
        hashVel1, _, next_vec_hash_value = getVectorHash(vecHash, moons[1].velocity, next_vec_hash_value)
        hashPos2, _, next_vec_hash_value = getVectorHash(vecHash, moons[2].position, next_vec_hash_value)
        hashVel2, _, next_vec_hash_value = getVectorHash(vecHash, moons[2].velocity, next_vec_hash_value)
        hashPos3, _, next_vec_hash_value = getVectorHash(vecHash, moons[3].position, next_vec_hash_value)
        hashVel3, _, next_vec_hash_value = getVectorHash(vecHash, moons[3].velocity, next_vec_hash_value)

        t = (hashPos0, hashPos1, hashPos2, hashPos3, hashVel0, hashVel1, hashVel2, hashVel3)

        _, existed, next_sys_hash_value = getVectorHash(sysHash, t, next_sys_hash_value)
    # _, existed, next_sys_hash_value = getVectorHash(sysHash, systemStatus, next_sys_hash_value)
    # return existed, next_sys_hash_value, next_vec_hash_value
    return existed, next_sys_hash_value, next_vec_hash_value

def getRepeatedStatus(moons, max_iters = None):
    vector_hash = {}
    system_hash = {}
    # vector_hash = shelve.open(r'c:\tmp\vector_hash')
    # system_hash = shelve.open(r'c:\tmp\system_hash')
    # vector_hash.clear()
    # vector_hash.close()
    # system_hash.clear()
    # system_hash.close()
    # vector_hash = shelve.open(r'c:\tmp\vector_hash')
    # system_hash = shelve.open(r'c:\tmp\system_hash')


    next_vec_hash_value = 0
    next_sys_hash_value = 0

    num_moons = len(moons)

    _, next_sys_hash_value, next_vec_hash_value = hashSystem(system_hash, vector_hash, moons, num_moons, next_sys_hash_value, next_vec_hash_value)
    print(f'Estado 0. E. total {sum([m.getTotalEnergy() for m in moons])} E.potencial {sum([m.getPotentialEnergy() for m in moons])} E.cinética {sum([m.getKineticEnergy() for m in moons])}')

    #max_iters = 10000
    encontrado = False
    #for iter in range(1, max_iters):
    iter = 0


    while True:
        iter += 1
        updateMoons(moons, num_moons)
        existed, next_sys_hash_value, next_vec_hash_value = hashSystem(system_hash, vector_hash, moons, num_moons, next_sys_hash_value, next_vec_hash_value)
        # print(f'Estado {iter}. E. total {sum([m.getTotalEnergy() for m in moons])} E.potencial {sum([m.getPotentialEnergy() for m in moons])} E.cinética {sum([m.getKineticEnergy() for m in moons])}')
        # if sum([m.getKineticEnergy() for m in moons]) == 0:
        #     for m in moons:
        #         m.printMoon()
        if existed:
            print(f'Encontrado estado repetido en iteración {iter}')
            encontrado = True
            break

        if max_iters is not None and iter > max_iters:
            print('Límite de iteraciones superado!')
            break

        if iter % 100000 == 0:
            print(f'| {datetime.now()} | Iteración {iter}. Vectores: {iter*8} En cache: {len(vector_hash)}. Tasa: {len(vector_hash)/(iter*8)}')

    # vector_hash.clear()
    # vector_hash.close()
    # system_hash.clear()
    # system_hash.close()

    return encontrado, iter

'''
def hashInner(rootHash, theKey):
    existo = True
    if theKey not in rootHash:
        existo = False
        rootHash[theKey] = {}
    return rootHash[theKey], existo

def hashSystem(rootHash, moons):
    theHash = rootHash
    systen_exists = True
    for m in moons:
        for i in range(len(m.position)):
            theHash, existo = hashInner(theHash, m.position[i])
            systen_exists &= existo
        for i in range(len(m.velocity)):
            theHash, existo = hashInner(theHash, m.velocity[i])
            systen_exists &= existo
    return systen_exists

def getRepeatedStatus(moons, max_iters = None):
    iter = 0

    root_hash = {}

    hashSystem(root_hash, moons)

    while True:
        iter += 1
        updateMoons(moons)
        existed = hashSystem(root_hash, moons)

        if existed:
            print(f'Encontrado estado repetido en iteración {iter}')
            encontrado = True
            break

        if max_iters is not None and iter > max_iters:
            print('Límite de iteraciones superado!')
            break

        if iter % 100000 == 0:
            print(f'| {datetime.now()} | Iteración {iter}.')

    return encontrado, iter
'''

'''
def hashMoon(vecHash, moon, next_vec_hash_value):
    arrayToHash = np.concatenate((moon.position, moon.velocity), axis=0)
    hashPos, _, next_vec_hash_value = getVectorHash(vecHash, arrayToHash, next_vec_hash_value)

    return hashPos, next_vec_hash_value

def hashSystem(sysHash, vecHash, moons, next_sys_hash_value ,next_vec_hash_value):
    systemStatus = np.zeros(len(moons))

    for i in range(len(moons)):
        m = moons[i]
        hashPos, next_vec_hash_value = hashMoon(vecHash, m, next_vec_hash_value)
        systemStatus[i] = hashPos

    _, existed, next_sys_hash_value = getVectorHash(sysHash, systemStatus, next_sys_hash_value)
    return existed, next_sys_hash_value, next_vec_hash_value

def getRepeatedStatus(moons, max_iters = None):
    vector_hash = {}
    system_hash = {}

    next_vec_hash_value = 0
    next_sys_hash_value = 0

    _, next_sys_hash_value, next_vec_hash_value = hashSystem(system_hash, vector_hash, moons, next_sys_hash_value, next_vec_hash_value)

    #max_iters = 10000
    encontrado = False
    #for iter in range(1, max_iters):
    iter = 0

    while True:
        iter += 1
        updateMoons(moons)
        existed, next_sys_hash_value, next_vec_hash_value = hashSystem(system_hash, vector_hash, moons, next_sys_hash_value, next_vec_hash_value)

        if existed:
            print(f'Encontrado estado repetido en iteración {iter}')
            encontrado = True
            break

        if max_iters is not None and iter > max_iters:
            print('Límite de iteraciones superado!')
            break

        if iter % 100000 == 0:
            print(f'| {datetime.now()} | Iteración {iter}. Vectores: {iter*4} En cache: {len(vector_hash)}. Tasa: {len(vector_hash)/(iter*4)}')

    return encontrado, iter
'''

import yappi

#TEST 1
rawMoons = '<x=-1, y=0, z=2>\n\
<x=2, y=-10, z=-7>\n\
<x=4, y=-8, z=8>\n\
<x=3, y=5, z=-1>'

moons = [m.Moon.parseMoon(str(i), rawmoon) for i, rawmoon in enumerate(rawMoons.split('\n'))]

isFound, step = getRepeatedStatus(moons)


#TEST 2
rawMoons = '<x=-8, y=-10, z=0>\n\
<x=5, y=5, z=10>\n\
<x=2, y=-7, z=3>\n\
<x=9, y=-8, z=-3>'

moons = [m.Moon.parseMoon(str(i), rawmoon) for i, rawmoon in enumerate(rawMoons.split('\n'))]

# yappi.set_clock_type("wall")
# yappi.start(builtins=True)

isFound, step = getRepeatedStatus(moons)

# yappi.get_func_stats().print_all()
# yappi.get_thread_stats().print_all()
# callgrind_filename = f'callgrind.filename.{datetime.now().strftime("%Y%m%d_%H%M%S")}.prof'
# stats = yappi.get_func_stats()
# stats.save(rf'C:\Users\rodrigo\PyCharmProjects\aoc2019-day12\{callgrind_filename}', type='callgrind')

exit(0)

#SOLUTION
input_12 = r'data\aoc2019-input-day12.txt'
data12=[]
with open(input_12, 'r') as f:
    data12 = [m.Moon.parseMoon(str(number), data) for number, data in enumerate(f.readlines()) if len(data) > 0]

# print(f'| {datetime.now()} | ssss')
# updateSteps(data12, 12000000)
# print(f'| {datetime.now()} | ssss')

print(f'| {datetime.now()} | Empezamossss')
isFound, step = getRepeatedStatus(data12)
print(f'| {datetime.now()} | Terminamossss')

