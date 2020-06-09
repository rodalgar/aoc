import numpy as np
from Intcode.IntcodeDevice import IntcodeDevice

from LevelMap import Tile


class JoystickDevice(IntcodeDevice):
    attached_to = None

    def attach_to(self, to):
        self.attached_to = to

    def getNewDirection(self):
        while True:
            rawinput = input(f'[{self.label}] Input direction (W, A, S, D):')
            n = rawinput.upper()
            if n in ['W', 'A', 'S', 'D']:
                break
            else:
                print(f'[{self.label}] direction {rawinput} is invalid!')

        direction = None
        if n == 'W':
            direction = 1
        elif n == 'A':
            direction = 3
        elif n == 'S':
            direction = 2
        else:
            direction = 4

        return direction

    def read(self):
        assert self.attached_to is not None, f'[{self.label}] Device is not attached to anything!!'

        self.attached_to.level_map.print_screen()

        direction = self.getNewDirection()

        self.attached_to.begin_movement(direction)

        # Returning transformed input
        return direction


class AutomaticJoystickDevice(JoystickDevice):
    last_direction = None
    are_we_backtracking = None

    def __init__(self, label):
        super().__init__(label)
        self.are_we_backtracking = False

    def get_valid_direction(self):
        the_map = self.attached_to.level_map

        # we try clock-wise
        self.are_we_backtracking = False
        if the_map.get_tile_at_direction(the_map.DIRECTION_NORTH).tile_type == Tile.TYPE_UNK:
            return 1
        elif the_map.get_tile_at_direction(the_map.DIRECTION_EAST).tile_type == Tile.TYPE_UNK:
            return 4
        elif the_map.get_tile_at_direction(the_map.DIRECTION_SOUTH).tile_type == Tile.TYPE_UNK:
            return 2
        elif the_map.get_tile_at_direction(the_map.DIRECTION_WEST).tile_type == Tile.TYPE_UNK:
            return 3

        # If we reach this point, there is no unknown tile to scout from the actual one.
        # Most likely reason for this is we found a cul-de-sac or we are already backtracking from one.
        # So, we will select our adjacent with the lesser cost.
        self.are_we_backtracking = True

        minimun_cost = np.inf
        best_direction = None
        for direction in [the_map.DIRECTION_NORTH, the_map.DIRECTION_EAST, the_map.DIRECTION_SOUTH, the_map.DIRECTION_WEST]:
            tile = the_map.get_tile_at_direction(direction)
            if tile.tile_type == Tile.TYPE_FLOOR:
                if tile.minimum_cost < minimun_cost:
                    minimun_cost = tile.minimum_cost
                    best_direction = the_map.get_direction_from_vector(direction)

        # print('BACKTRACK!!!', best_direction)

        return best_direction

    def getNewDirection(self):
        last_navigation_result = self.attached_to.get_last_navigation_result()

        if last_navigation_result == SensorDevice.SENSOR_RESULT_BLOCK:
            self.last_direction = self.get_valid_direction()
            new_direction = self.last_direction
        else:
            if self.last_direction is None or self.are_we_backtracking:
                self.last_direction = self.get_valid_direction()
            new_direction = self.last_direction
        return new_direction


class SensorDevice(IntcodeDevice):
    attached_to = None

    SENSOR_RESULT_BLOCK = 0
    SENSOR_RESULT_FLOOR = 1
    SENSOR_RESULT_GOAL = 2

    def attach_to(self, to):
        self.attached_to = to

    def write(self, data):
        assert 0 <= data <= 2, f'[{self.label}] Unknown navigation result {data}!!!'
        print(f'[{self.label}] received {data}')

        self.attached_to.resolve_movement(data)