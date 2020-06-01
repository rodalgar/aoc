class IntcodeParameter():
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

    value = None
    mode = None

    def __init__(self, value, mode):
        self.value = value
        self.mode = mode
        assert mode in [IntcodeParameter.POSITION, IntcodeParameter.IMMEDIATE, IntcodeParameter.RELATIVE], \
            f'UNKNOWN PARAMETER MODE {mode}'

    def checkBoundedParameter(self, program):
        if self.mode == IntcodeParameter.POSITION:
            assert self.value >= 0 and self.value < len(program.code), \
                f'position parameter out of bounds. Position: {self.value}, Program size {len(program.code)}'
        elif self.mode == IntcodeParameter.RELATIVE:
            realPos = self.value + program.relative_base
            assert realPos >= 0 and realPos < len(program.code), \
                'relative parameter out of bounds. Position: {self.value}, Relative base {program.relative_base}, Program size {len(program.code)}'
        return True

    def evaluateParameter(self, program):
        if self.mode == IntcodeParameter.POSITION:
            return program.code[self.value]
        elif self.mode == IntcodeParameter.IMMEDIATE:
            return self.value
        elif self.mode == IntcodeParameter.RELATIVE:
            return program.code[self.value + program.relative_base]
        else:
            raise Exception('UNKNOWN PARAMETER MODE {}. Value {}. Program {}'.format(self.mode, self.value, program))

    def getParameterPosition(self, program):
        if self.mode == IntcodeParameter.POSITION:
            return self.value
        elif self.mode == IntcodeParameter.RELATIVE:
            return self.value + program.relative_base
        elif self.mode == IntcodeParameter.IMMEDIATE:
            raise Exception(f'Immediate parameter mode {self.value} cannot be used as position!')
        else:
            raise Exception(f'UNKNOWN PARAMETER MODE {self.mode}. Value {self.value}. Program {program}')

    def toString(self, program):
        return '[value {}, mode {}, evaluation {}]'.format(self.value, self.mode, self.evaluateParameter(program))