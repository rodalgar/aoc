import numpy as np


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