import numpy as np
import math
import re


class Moon:
    position = None
    velocity = None
    label = None
    gravityForce = None

    def __sign(x):
        return 0 if x == 0 else 1 if x > 0 else -1

    # def __init__(self, label, starting_position=np.zeros(3, dtype=int)):
    def __init__(self, label, starting_position=(0, 0, 0)):
        self.label = label
        self.position = starting_position
        # self.velocity = np.zeros(3, dtype=int)
        # self.gravityForce = np.zeros(3, dtype=int)
        self.velocity = (0, 0, 0)
        self.gravityForce = (0, 0, 0)

    # def getGravityPull(self, anotherMoon):
    #     pull = (self.position < anotherMoon.position).astype(int)
    #     push = (self.position > anotherMoon.position).astype(int)
    #
    #     return pull - push

    def getGravityPull(self, anotherMoon):

        # return tuple(math.copysign(1, q - p) for p, q in zip(self.position, anotherMoon.position))
        return tuple(Moon.__sign(q-p) for p, q in zip(self.position, anotherMoon.position))


    def getPotentialEnergy(self):
        return np.sum(np.abs(self.position))

    def getKineticEnergy(self):
        return np.sum(np.abs(self.velocity))

    def getTotalEnergy(self):
        return self.getPotentialEnergy() * self.getKineticEnergy()

    def printMoon(self):
        print(f'pos=<x={self.position[0]:3}, y={self.position[1]:3}, z={self.position[2]:3}>, vel=<x={self.velocity[0]:3}, y={self.velocity[1]:3}, z={self.velocity[2]:3}>')
        print(f'pot. Energy: {self.getPotentialEnergy()}, kin. Energy: {self.getKineticEnergy()}, tot. Energy: {self.getTotalEnergy()}')

    def parseMoon(label, rawdata):
        #RawData sample:
        #<x=-1, y=7, z=3>
        x = re.search('x=(-*[0-9]+)', rawdata).groups(1)[0]
        # print('x vale', x)
        y = re.search('y=(-*[0-9]+)', rawdata).groups(1)[0]
        # print('y vale', y)
        z = re.search('z=(-*[0-9]+)', rawdata).groups(1)[0]
        # print('z vale', z)

        # return Moon(label, np.array([int(x), int(y), int(z)], dtype=int))
        return Moon(label, (int(x), int(y), int(z)))