from LevelMap import LevelMap, Tile
from ProblemDevices import SensorDevice


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