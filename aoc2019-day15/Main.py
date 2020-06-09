from Intcode.IntcodeMachine import IntcodeInterpreterV5

from ProblemDevices import AutomaticJoystickDevice, SensorDevice
from RepairDroid import RepairDroid

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