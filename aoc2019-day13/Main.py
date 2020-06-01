import time
from collections import Counter

from IntcodeDevice import IntcodeDevice
from IntcodeMachine import IntcodeInterpreterV5


class ArcadeCabinet():
    machine = None
    screen = None
    joystick = None
    program = None

    tile_map = None

    score = None
    x_ball = None
    x_paddle = None

    def __init__(self, machine, screen, joystick):
        self.tile_map = {}
        self.machine = machine
        self.screen = screen
        self.joystick = joystick

        self.screen.attach_to(self)
        self.joystick.attach_to(self)

        self.machine.instructions[3].setDevice(self.joystick)
        self.machine.instructions[4].setDevice(self.screen)

    def loadGame(self, program):
        self.program = program

    def __new_tile(self, tile):
        (col, line, tile_type) = tile

        if line not in self.tile_map:
            self.tile_map[line] = {}

        self.tile_map[line][col] = tile_type

        if tile_type == 3:
            self.x_paddle = col
        elif tile_type ==4:
            self.x_ball = col

    def __count_death(self, command):
        (_, _, self.score) = command

    def read_screen(self, command):
        (command_type, command_subtype, _) = command

        # print(command)

        if command_type == -1:
            if command_subtype == 0:
                self.__count_death(command)
            else:
                print('COMMAND!!', command)
                exit(0)
        else:
            self.__new_tile(command)

    def print_screen(self):
        max_line = -1
        max_col = -1
        for line in arcade.tile_map:
            if line > max_line:
                max_line = line
            for col in arcade.tile_map[line]:
                if col > max_col:
                    max_col = col

        # print('print_screen', max_line, max_col)

        for line in range(max_line+1):
            str_line = ''
            for col in range(max_col+1):
                valor = arcade.tile_map[line][col]
                if valor == 0:
                    str_line += ' '
                elif valor == 1:
                    str_line += '#'
                elif valor == 2:
                    str_line += '&'
                elif valor == 3:
                    str_line += '-'
                elif valor == 4:
                    str_line += 'o'
                else:
                    raise Exception(f'tile type is UNKNOWN!! {valor}')
            print(str_line)
        print('Score:', self.score)

    def getGameData(self):
        return self.x_paddle, self.x_ball

    def play(self, infinite_coins=False):
        assert self.program is not None, 'There is no game loaded yet!!'

        program = self.program
        if infinite_coins:
            program[0] = 2

        print('Begin play!!')
        self.score = 0
        self.machine.compute(program)
        print('Game over!')
        print('Score:', self.score)


class ScreenDevice(IntcodeDevice):
    attached_to = None
    buffer = None

    def __init__(self, label):
        super().__init__(label)
        self.buffer = []

    def attach_to(self, to):
        self.attached_to = to

    def write(self, data):
        assert self.attached_to is not None, 'screen is not attached to anything!!'

        self.buffer.append(data)

        if len(self.buffer) == 3:
            self.attached_to.read_screen(tuple(self.buffer))
            self.buffer.clear()

class JoystickDevice(IntcodeDevice):
    attached_to = None

    def attach_to(self, to):
        self.attached_to = to

    def read(self):
        assert self.attached_to is not None, 'joystick is not attached to anything!!'

        self.attached_to.print_screen()

        n = input(f'[{self.label}] Solicitando dato de entrada (1, 2 ó 3):')

        try:
            data = int(n)
        except ValueError:
            raise Exception(f'[{self.label}] read [{n}] that is not an int!!')

        if data < 1 or data > 3:
            print(f'[{self.label}] input data should be 1, 2 or 3')
            data = 2

        # Returning transformed input
        return data - 2


class AutomaticJoystickDevice(JoystickDevice):
    def read(self):
        self.attached_to.print_screen()
        # time.sleep(1)
        x_paddle, x_ball = self.attached_to.getGameData()

        if x_paddle > x_ball:
            return -1
        elif x_paddle < x_ball:
            return 1
        else:
            return 0


# PART 1:
# Initializing the new Arcade Cabinet!!
arcade = ArcadeCabinet(IntcodeInterpreterV5(), ScreenDevice('screen'), JoystickDevice('joystick'))

# Getting game from disk and loading it into the cabinet!
input_13 = r'data\aoc2019-input-day13.txt'
with open(input_13, 'r') as f:
    data13 = [int(data) for data in f.read().split(',') if len(data) > 0]

arcade.loadGame(data13)

# Playing the game!
arcade.play()

# Analyzing game
number_of_tiles = Counter()
for line in arcade.tile_map:
    for col in arcade.tile_map[line]:
        number_of_tiles[arcade.tile_map[line][col]] += 1

print('Tiles', number_of_tiles, 'Blocks', number_of_tiles[2])

# SOLUTION: >>>255

# PART 2:
arcade = ArcadeCabinet(IntcodeInterpreterV5(), ScreenDevice('screen'), AutomaticJoystickDevice('joystick'))
arcade.loadGame(data13)
arcade.play(infinite_coins=True)

# SOLUTION: >>>12338