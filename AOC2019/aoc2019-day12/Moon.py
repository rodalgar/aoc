import numpy as np
import math
import re


class Moon:
    position = None
    velocity = None
    label = None
    gravity_force = None

    @staticmethod
    def __sign(x):
        return 0 if x == 0 else 1 if x > 0 else -1

    def __init__(self, label, starting_position=(0, 0, 0)):
        self.label = label
        self.position = starting_position
        self.velocity = (0, 0, 0)
        self.gravity_force = (0, 0, 0)

    def get_gravity_pull(self, another_moon):
        return tuple(Moon.__sign(q - p) for p, q in zip(self.position, another_moon.position))

    def get_potential_energy(self):
        return np.sum(np.abs(self.position))

    def get_kinetic_energy(self):
        return np.sum(np.abs(self.velocity))

    def get_total_energy(self):
        return self.get_potential_energy() * self.get_kinetic_energy()

    def print_moon(self):
        print(f'pos=<x={self.position[0]:3}, y={self.position[1]:3}, z={self.position[2]:3}>, '
              f'vel=<x={self.velocity[0]:3}, y={self.velocity[1]:3}, z={self.velocity[2]:3}>')
        print(f'pot. Energy: {self.get_potential_energy()}, '
              f'kin. Energy: {self.get_kinetic_energy()}, '
              f'tot. Energy: {self.get_total_energy()}')

    @staticmethod
    def parse_moon(label, raw_data):
        # RawData sample:
        # <x=-1, y=7, z=3>
        x = re.search('x=(-*[0-9]+)', raw_data).groups(1)[0]
        # print('x vale', x)
        y = re.search('y=(-*[0-9]+)', raw_data).groups(1)[0]
        # print('y vale', y)
        z = re.search('z=(-*[0-9]+)', raw_data).groups(1)[0]
        # print('z vale', z)

        return Moon(label, (int(x), int(y), int(z)))
