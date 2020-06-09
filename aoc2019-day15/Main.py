import numpy as np
from Intcode.IntcodeDevice import IntcodeDevice
from Intcode.IntcodeMachine import IntcodeInterpreterV5


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

        self.attached_to.print_screen()
        #DEBUGGG
        print(self.attached_to.unexplored_tiles)

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

    def get_coords_at_direction(self, direction):
        new_direction = self.attached_to.actual_position + direction
        return (new_direction[0], new_direction[1])

    def get_tile_at_direction(self, the_map, direction):
        # new_pos = self.attached_to.actual_position + direction
        new_pos = self.get_coords_at_direction(direction)
        return the_map[new_pos[0], new_pos[1]]

    def check_if_direction_is_valid(self, the_map, direction, tile_type):
        return self.get_tile_at_direction(the_map, direction).tile_type == tile_type

    def get_valid_direction(self):
        print('get_valid_direction', 'INVOCADA')
        #TODO: First version: try first unknown tile.
        # self.attached_to.actual_map
        # self.attached_to.actual_position
        # y, x = self.attached_to.actual_position[0], self.attached_to.actual_position[1]
        the_map = self.attached_to.actual_map

        # we try clock-wise
        self.are_we_backtracking = False
        if self.check_if_direction_is_valid(the_map, self.attached_to.DIRECTION_NORTH, Tile.TYPE_UNK):
            return 1
        elif self.check_if_direction_is_valid(the_map, self.attached_to.DIRECTION_EAST, Tile.TYPE_UNK):
            return 4
        elif self.check_if_direction_is_valid(the_map, self.attached_to.DIRECTION_SOUTH, Tile.TYPE_UNK):
            return 2
        elif self.check_if_direction_is_valid(the_map, self.attached_to.DIRECTION_WEST, Tile.TYPE_UNK):
            return 3

        # If we reach this point, there is no unknown tile to scout from the actual one.
        # Most likely reason for this is we found a cul-de-sac or we are already backtracking from one.
        # So, we will select our adjacent with the lesser cost.
        self.are_we_backtracking = True

        minimun_cost = np.inf
        best_direction = None
        for direction in [self.attached_to.DIRECTION_NORTH, self.attached_to.DIRECTION_EAST, self.attached_to.DIRECTION_SOUTH, self.attached_to.DIRECTION_WEST]:
            tile = self.get_tile_at_direction(the_map, direction)
            if tile.tile_type == Tile.TYPE_FLOOR:
                if tile.minimum_cost < minimun_cost:
                    minimun_cost = tile.minimum_cost
                    best_direction = self.attached_to.get_direction_from_vector(direction)

        print('BACKTRACK!!!', best_direction)

        return best_direction

    def get_unexplored_adjacent_tiles(self, the_map):
        for direction in [self.attached_to.DIRECTION_NORTH, self.attached_to.DIRECTION_EAST, self.attached_to.DIRECTION_SOUTH, self.attached_to.DIRECTION_WEST]:
            if self.get_tile_at_direction(the_map, direction).tile_type == Tile.TYPE_UNK:
                self.attached_to.unexplored_tiles.add(self.get_coords_at_direction(direction))

    def getNewDirection(self):
        last_navigation_result = self.attached_to.get_last_navigation_result()

        # Managing unexplored tiles. Adding new unexplored adjacent tiles and removing explored ones.
        t_position = (self.attached_to.actual_position[0], self.attached_to.actual_position[1])
        self.get_unexplored_adjacent_tiles(self.attached_to.actual_map)

        if last_navigation_result == SensorDevice.SENSOR_RESULT_BLOCK:
            self.attached_to.unexplored_tiles.remove(self.get_coords_at_direction(self.last_direction))

            self.last_direction = self.get_valid_direction()
            new_direction = self.last_direction
        # elif last_navigation_result == SensorDevice.SENSOR_RESULT_FLOOR:
        else:
            if t_position in self.attached_to.unexplored_tiles:
                self.attached_to.unexplored_tiles.remove(t_position)

            if self.last_direction is None or self.are_we_backtracking:
                self.last_direction = self.get_valid_direction()
            new_direction = self.last_direction
        # else:
        #     print('Hemos llegado al destino!!!! bwahahahaha')
        #     self.attached_to.print_screen()
        #     # exit(0)
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


class Tile():
    tile_type = None
    minimum_cost = np.inf

    TYPE_UNK    = 0
    TYPE_BLOCK  = 1
    TYPE_FLOOR  = 2

    def __init__(self, type):
        assert type in [Tile.TYPE_UNK, Tile.TYPE_BLOCK, Tile.TYPE_FLOOR], f'Unknown tile type {type}!'
        self.tile_type = type

    def get_tile_symbol(self):
        if self.tile_type == Tile.TYPE_BLOCK:
            return '#'
        elif self.tile_type == Tile.TYPE_FLOOR:
            return '.'
        else:
            return '?' #TODO: Change this for ' '

    def __repr__(self):
        return f'{self.get_tile_symbol()} {self.minimum_cost}'


class RepairDroid():

    machine = None
    program = None
    joystick = None
    sensor = None

    actual_map = None
    actual_direction = None
    actual_position = None

    last_navigation_result = None
    unexplored_tiles = None

    # MAP_MAX_X = 80
    # MAP_MAX_Y = 40
    MAP_MAX_X = 100
    MAP_MAX_Y = 50

    DIRECTION_NORTH = np.array((-1, 0), dtype=int)
    DIRECTION_SOUTH = np.array((1, 0), dtype=int)
    DIRECTION_WEST = np.array((0, -1), dtype=int)
    DIRECTION_EAST = np.array((0, 1), dtype=int)

    def __init__(self, machine, program, joystick, sensor):
        self.machine = machine
        self.program = program
        self.joystick = joystick
        self.sensor = sensor

        self.joystick.attach_to(self)
        self.sensor.attach_to(self)

        self.machine.instructions[3].setDevice(self.joystick)
        self.machine.instructions[4].setDevice(self.sensor)

    def print_screen(self):
        print('print_screen')
        # return
        for y in range(0, RepairDroid.MAP_MAX_Y):
            row = ''
            for x in range(0, RepairDroid.MAP_MAX_X):
                if self.actual_position[0] == y and self.actual_position[1] == x:
                    row += '@'
                else:
                    row += self.actual_map[y, x].get_tile_symbol()
            print(row)
        print('Actual position:', self.actual_position)

    def get_last_navigation_result(self):
        return self.last_navigation_result

    def get_direction_from_index(self, direction):
        assert 0 < direction < 5, f"Can't convert direction {direction}!!"
        if direction == 1:
            return RepairDroid.DIRECTION_NORTH
        elif direction == 2:
            return RepairDroid.DIRECTION_SOUTH
        elif direction == 3:
            return RepairDroid.DIRECTION_WEST
        else:
            return RepairDroid.DIRECTION_EAST

    def get_direction_from_vector(self, direction):
        if np.array_equal(direction, self.DIRECTION_NORTH):
            return 1
        elif np.array_equal(direction, self.DIRECTION_SOUTH):
            return 2
        elif np.array_equal(direction, self.DIRECTION_WEST):
            return 3
        else:
            return 4

    def move_to(self, new_position, new_cost):
        assert 0 <= new_position[0] < self.MAP_MAX_Y, f'Y Axis is out of bounds! {new_position}'
        assert 0 <= new_position[1] < self.MAP_MAX_X, f'X Axis is out of bounds! {new_position}'

        self.actual_position = new_position
        if self.last_navigation_result is None:
            self.last_navigation_result = SensorDevice.SENSOR_RESULT_FLOOR
        # print('move_to', f'moviendo a {new_position}')
        if self.actual_map[new_position[0], new_position[1]].tile_type == Tile.TYPE_UNK:
            self.actual_map[new_position[0], new_position[1]] = Tile(Tile.TYPE_FLOOR)
            self.actual_map[new_position[0], new_position[1]].minimum_cost = new_cost
        elif self.actual_map[new_position[0], new_position[1]].tile_type == Tile.TYPE_FLOOR:
            # actualizamos el coste
            if self.actual_map[new_position[0], new_position[1]].minimum_cost > new_cost:
                print(f'Llegar a {new_position[0]},{new_position[1]} costaba {self.actual_map[new_position[0], new_position[1]].minimum_cost} pero ahora cuesta {new_cost}!')
                self.actual_map[new_position[0], new_position[1]].minimum_cost = new_cost

    def resolve_movement(self, navigation_result):
        # print('resolve_movement', navigation_result)
        self.last_navigation_result = navigation_result
        new_cost = self.actual_map[self.actual_position[0], self.actual_position[1]].minimum_cost + 1
        new_position = self.actual_position + self.actual_direction

        if navigation_result == SensorDevice.SENSOR_RESULT_BLOCK:
            #block found at new position
            self.actual_map[new_position[0], new_position[1]] = Tile(Tile.TYPE_BLOCK)
        elif navigation_result == SensorDevice.SENSOR_RESULT_FLOOR:
            #floor
            self.move_to(new_position, new_cost)
        else:
            #goal
            self.move_to(new_position, new_cost)

    def begin_movement(self, direction):
        # print('begin_movement', direction)
        # TODO: Hacer aquí el chequeo del tamaño para ver si hay que ampliar el mapa
        self.actual_direction = self.get_direction_from_index(direction)

    def searchOxygenSystem(self):
        self.unexplored_tiles = set()
        self.actual_map = np.full([RepairDroid.MAP_MAX_Y, RepairDroid.MAP_MAX_X], Tile(Tile.TYPE_UNK))
        self.move_to(np.array([RepairDroid.MAP_MAX_Y // 2, RepairDroid.MAP_MAX_X // 2], dtype=int), 0)

        print('AA')
        self.print_screen()
        print('BB')
        # zaska = self.machine.compute(self.program)
        if self.machine.program is None:
            self.machine.beginStep(self.program)
        while self.last_navigation_result != SensorDevice.SENSOR_RESULT_GOAL:
            self.machine.nextStep()
        print('CC')
        final_tile = self.actual_map[self.actual_position[0], self.actual_position[1]]
        print(f'Coste de llegar al fin es {final_tile.minimum_cost}')
        return final_tile.minimum_cost

    def traverse_all_map(self):
        while len(self.unexplored_tiles) > 0:
            self.machine.nextStep()

    def get_time_for_full_oxygen(self):
        self.traverse_all_map()
        self.print_screen()

        return -1


input_15 = r'data\aoc2019-input-day15.txt'
with open(input_15, 'r') as f:
    data15 = [int(data) for data in f.read().split(',') if len(data) > 0]


##################
# PART 1 #########
##################
repairDroid = RepairDroid(IntcodeInterpreterV5(), data15, AutomaticJoystickDevice('joystick'), SensorDevice('sensor'))
cost = repairDroid.searchOxygenSystem()
print('Minimum cost is', cost)

#>>>SOLUTION: 214

print('THE END')

##################
# PART 2 #########
##################
minutes = repairDroid.get_time_for_full_oxygen()
