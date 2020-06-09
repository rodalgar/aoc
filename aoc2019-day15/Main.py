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


class Tile():
    tile_type = None
    minimum_cost = None
    with_oxygen = False

    TYPE_UNK    = 0
    TYPE_BLOCK  = 1
    TYPE_FLOOR  = 2

    def __init__(self, tile_type, min_cost=np.inf):
        assert tile_type in [Tile.TYPE_UNK, Tile.TYPE_BLOCK, Tile.TYPE_FLOOR], f'Unknown tile type {tile_type}!'
        self.tile_type = tile_type
        self.minimum_cost = min_cost

    def get_tile_symbol(self):
        if self.tile_type == Tile.TYPE_BLOCK:
            return '#'
        elif self.tile_type == Tile.TYPE_FLOOR and not self.with_oxygen:
            return '.'
        elif self.tile_type == Tile.TYPE_FLOOR and self.with_oxygen:
            return 'O'
        else:
            return ' '

    def __repr__(self):
        return f'{self.get_tile_symbol()} {self.minimum_cost}'


class LevelMap():
    actual_map = None
    actual_direction = None
    actual_position = None
    goal_position = None

    unexplored_tiles = None

    MAP_MAX_X = None
    MAP_MAX_Y = None

    DIRECTION_NORTH = np.array((-1, 0), dtype=int)
    DIRECTION_SOUTH = np.array((1, 0), dtype=int)
    DIRECTION_WEST = np.array((0, -1), dtype=int)
    DIRECTION_EAST = np.array((0, 1), dtype=int)

    def __init__(self, max_x, max_y):
        self.MAP_MAX_X = max_x
        self.MAP_MAX_Y = max_y

    def initialize_map(self):
        self.unexplored_tiles = set()
        self.actual_map = np.full([self.MAP_MAX_Y, self.MAP_MAX_X], Tile(Tile.TYPE_UNK))
        self.actual_position = np.array((self.MAP_MAX_Y // 2, self.MAP_MAX_X // 2), dtype=int)
        self.actual_map[self.actual_position[0], self.actual_position[1]] = Tile(Tile.TYPE_FLOOR, 0)
        self.update_unexplored_tiles()

    def get_direction_from_index(self, direction):
        assert 0 < direction < 5, f"Can't convert direction {direction}!!"
        if direction == 1:
            return self.DIRECTION_NORTH
        elif direction == 2:
            return self.DIRECTION_SOUTH
        elif direction == 3:
            return self.DIRECTION_WEST
        else:
            return self.DIRECTION_EAST

    def get_direction_from_vector(self, direction):
        if np.array_equal(direction, self.DIRECTION_NORTH):
            return 1
        elif np.array_equal(direction, self.DIRECTION_SOUTH):
            return 2
        elif np.array_equal(direction, self.DIRECTION_WEST):
            return 3
        else:
            return 4

    def get_coords_at_direction(self, direction):
        new_direction = self.actual_position + direction
        return (new_direction[0], new_direction[1])

    def get_tile_at_direction(self, direction):
        new_pos = self.get_coords_at_direction(direction)
        return self.get_tile_at_position(new_pos[0], new_pos[1])

    def get_tile_at_position(self, y, x):
        return self.actual_map[y, x]

    def get_actual_tile(self):
        return self.actual_map[self.actual_position[0], self.actual_position[1]]

    def print_screen(self):
        for y in range(0, self.MAP_MAX_Y):
            row = ''
            for x in range(0, self.MAP_MAX_X):
                if self.actual_position[0] == y and self.actual_position[1] == x:
                    row += '@'
                elif self.goal_position is not None and self.goal_position[0] == y and self.goal_position[1] == x:
                    row += '*'
                else:
                    row += self.actual_map[y, x].get_tile_symbol()
            print(row)
        print('Actual position:', self.actual_position)
        print('Goal position:', self.goal_position)

    def begin_movement(self, direction):
        self.actual_direction = self.get_direction_from_index(direction)

    def update_unexplored_tiles(self):
        t_position = (self.actual_position[0], self.actual_position[1])
        if t_position in self.unexplored_tiles:
            self.unexplored_tiles.remove(t_position)

        for direction in [self.DIRECTION_NORTH, self.DIRECTION_EAST, self.DIRECTION_SOUTH, self.DIRECTION_WEST]:
            if self.get_tile_at_direction(direction).tile_type == Tile.TYPE_UNK:
                self.unexplored_tiles.add(self.get_coords_at_direction(direction))

    def movement_success(self, goal_found=False):
        new_position = self.actual_position + self.actual_direction
        new_cost = self.actual_map[self.actual_position[0], self.actual_position[1]].minimum_cost + 1

        assert 0 <= new_position[0] < self.MAP_MAX_Y, f'Y Axis is out of bounds! {new_position}'
        assert 0 <= new_position[1] < self.MAP_MAX_X, f'X Axis is out of bounds! {new_position}'

        self.actual_position = new_position
        if goal_found:
            self.goal_position = new_position

        # Manage unexplored tiles. Remove new position. Add adjacent from new_position
        self.update_unexplored_tiles()
        if self.actual_map[new_position[0], new_position[1]].tile_type == Tile.TYPE_UNK:
            self.actual_map[new_position[0], new_position[1]] = Tile(Tile.TYPE_FLOOR, new_cost)
        elif self.actual_map[new_position[0], new_position[1]].tile_type == Tile.TYPE_FLOOR:
            if self.actual_map[new_position[0], new_position[1]].minimum_cost > new_cost:
                print(f'Getting to {new_position[0]},{new_position[1]} had a cost of {self.actual_map[new_position[0], new_position[1]].minimum_cost}. Now costs {new_cost}!')
                self.actual_map[new_position[0], new_position[1]].minimum_cost = new_cost

    def movement_blocked(self):
        new_position = self.actual_position + self.actual_direction
        self.actual_map[new_position[0], new_position[1]] = Tile(Tile.TYPE_BLOCK)
        t_position = (new_position[0], new_position[1])
        if t_position in self.unexplored_tiles:
            self.unexplored_tiles.remove(t_position)

    def get_adjacent_coords_at_position(self, y, x):
        param_pos = np.array((y, x), dtype=int)

        return [tuple(param_pos + direction) for direction in [self.DIRECTION_NORTH, self.DIRECTION_EAST, self.DIRECTION_SOUTH, self.DIRECTION_WEST]]


class RepairDroid():

    machine = None
    program = None
    joystick = None
    sensor = None

    level_map = None
    last_navigation_result = None

    def __init__(self, machine, program, joystick, sensor):
        self.machine = machine
        self.program = program
        self.joystick = joystick
        self.sensor = sensor
        self.level_map = LevelMap(100, 50)

        self.joystick.attach_to(self)
        self.sensor.attach_to(self)

        self.machine.instructions[3].setDevice(self.joystick)
        self.machine.instructions[4].setDevice(self.sensor)

    def get_last_navigation_result(self):
        return self.last_navigation_result

    def move_to(self, new_position, new_cost):
        if self.last_navigation_result is None:
            self.last_navigation_result = SensorDevice.SENSOR_RESULT_FLOOR
        self.level_map.movement_success(new_position, new_cost)

    def resolve_movement(self, navigation_result):
        self.last_navigation_result = navigation_result

        if navigation_result == SensorDevice.SENSOR_RESULT_BLOCK:
            self.level_map.movement_blocked()
        elif navigation_result == SensorDevice.SENSOR_RESULT_FLOOR:
            #floor
            self.level_map.movement_success()
        else:
            #goal
            self.level_map.movement_success(goal_found=True)

    def begin_movement(self, direction):
        self.level_map.begin_movement(direction)

    def search_oxygen_system(self):
        self.level_map.initialize_map()

        self.level_map.print_screen()
        if self.machine.program is None:
            self.machine.beginStep(self.program)
        while self.last_navigation_result != SensorDevice.SENSOR_RESULT_GOAL:
            self.machine.nextStep()

        return self.level_map.get_actual_tile().minimum_cost

    def get_time_for_full_oxygen(self):
        # Traverse all map
        while len(self.level_map.unexplored_tiles) > 0:
            self.machine.nextStep()

        # Print initial state
        self.level_map.print_screen()

        minutes = -1

        processed_tiles = set()
        processing_queue = [tuple(self.level_map.goal_position)]

        while True:
            tmp_processing_queue = []
            while len(processing_queue) > 0:
                tile_coords = processing_queue[0]
                processing_queue = processing_queue[1:]
                if tile_coords in processed_tiles:
                    continue
                the_tile = self.level_map.get_tile_at_position(tile_coords[0], tile_coords[1])
                the_tile.with_oxygen = True
                processed_tiles.add(tile_coords)

                for adjacent in self.level_map.get_adjacent_coords_at_position(tile_coords[0], tile_coords[1]):
                    if adjacent in processed_tiles:
                        continue
                    adjacent_tile = self.level_map.get_tile_at_position(adjacent[0], adjacent[1])
                    if adjacent_tile.tile_type == Tile.TYPE_BLOCK:
                        continue
                    tmp_processing_queue.append(adjacent)

            minutes += 1
            self.level_map.print_screen()
            processing_queue = tmp_processing_queue
            if len(tmp_processing_queue) == 0:
                break

        return minutes


input_15 = r'data\aoc2019-input-day15.txt'
with open(input_15, 'r') as f:
    data15 = [int(data) for data in f.read().split(',') if len(data) > 0]


##################
# PART 1 #########
##################
repairDroid = RepairDroid(IntcodeInterpreterV5(), data15, AutomaticJoystickDevice('joystick'), SensorDevice('sensor'))
cost = repairDroid.search_oxygen_system()
print('Minimum cost is', cost)

#>>>SOLUTION: 214


##################
# PART 2 #########
##################
minutes = repairDroid.get_time_for_full_oxygen()

print('minutes:', minutes)

#>>>SOLUTION: 344