from .IntcodeDevice import ConsoleDevice
from .IntcodeParameter import IntcodeParameter


class IntcodeInstruction():
    endComputations = False
    parameters = []

    def mustEndComputations(self):
        return self.endComputations

    def getInstructionSize(self):
        return len(self.parameters) + 1  # parameters + opcode

    def getNextInstructionPointer(self, program):
        newIP = program.IP + self.getInstructionSize()
        assert newIP >= 0 and newIP < len(program.code), \
            f'new instruction pointer out of bounds. New IP {newIP}, last IP {program.IP}, Program size {len(program.code)}'
        return newIP

    def extractParameters(self, program):
        pass

    def performComputation(self, program):
        pass

    def checkParameters(self, program):
        for param in self.parameters:
            param.checkBoundedParameter(program)

    def __loadParameters(self, program):
        self.parameters = self.extractParameters(program)
        self.checkParameters(program)

    def compute(self, program):
        self.__loadParameters(program)
        self.performComputation(program)

    def toString(self, program):
        msg = f'{self.__class__.__name__} '
        for param in self.parameters:
            msg += param.toString(program)

        return (msg)


class OneParameterInst(IntcodeInstruction):
    def extractParameters(self, program):
        parameters = []
        modes = program.code[program.IP] // 100
        parameters.append(IntcodeParameter(program.code[program.IP + 1], modes % 10))

        return parameters


class TwoParametersInst(OneParameterInst):
    def extractParameters(self, program):
        parameters = super().extractParameters(program)
        modes = program.code[program.IP] // 100
        # 1 parameters + 1 result
        modes //= 10
        parameters.append(IntcodeParameter(program.code[program.IP + 2], modes % 10))

        return parameters


class ThreeParameterInst(TwoParametersInst):
    def extractParameters(self, program):
        parameters = super().extractParameters(program)
        modes = program.code[program.IP] // 100
        # 2 parameters + 1 result
        modes //= 10
        modes //= 10
        parameters.append(IntcodeParameter(program.code[program.IP + 3], modes % 10))

        return parameters


class IOInst(OneParameterInst):
    device = None

    def setDevice(self, device):
        self.device = device

    def getDevice(self):
        # for retro-compatibility reasons if no device was set, we set a new ConsoleDevice
        if self.device is None:
            self.device = ConsoleDevice()
            print(f'{self.__class__.__name__} had no device. Creating new {self.device.__class__.__name__}')

        return self.device


class AdditionInst(ThreeParameterInst):
    def performComputation(self, program):
        resultValue = self.parameters[0].evaluateParameter(program) + self.parameters[1].evaluateParameter(program)
        program.code[self.parameters[2].getParameterPosition(program)] = resultValue


class MultiplyInst(ThreeParameterInst):
    def performComputation(self, program):
        resultValue = self.parameters[0].evaluateParameter(program) * self.parameters[1].evaluateParameter(program)
        program.code[self.parameters[2].getParameterPosition(program)] = resultValue


class LessThanInst(ThreeParameterInst):
    def performComputation(self, program):
        resultValue = 0
        if self.parameters[0].evaluateParameter(program) < self.parameters[1].evaluateParameter(program):
            resultValue = 1
        program.code[self.parameters[2].getParameterPosition(program)] = resultValue


class EqualsInst(ThreeParameterInst):
    def performComputation(self, program):
        resultValue = 0
        if self.parameters[0].evaluateParameter(program) == self.parameters[1].evaluateParameter(program):
            resultValue = 1
        program.code[self.parameters[2].getParameterPosition(program)] = resultValue


class InputInst(IOInst):
    def performComputation(self, program):
        n = self.getDevice().read()

        program.code[self.parameters[0].getParameterPosition(program)] = int(n)


class OutputInst(IOInst):
    def performComputation(self, program):
        data = self.parameters[0].evaluateParameter(program)

        self.getDevice().write(data)


class JumpIfTrueInst(TwoParametersInst):
    def performComputation(self, program):
        #         print('JumpIfTrueInst!')
        pass

    def getNextInstructionPointer(self, program):
        if self.parameters[0].evaluateParameter(program) != 0:
            return self.parameters[1].evaluateParameter(program)

        return super().getNextInstructionPointer(program)


class JumpIfFalseInst(TwoParametersInst):
    def performComputation(self, program):
        #         print('JumpIfFalseInst!')
        pass

    def getNextInstructionPointer(self, program):
        if self.parameters[0].evaluateParameter(program) == 0:
            return self.parameters[1].evaluateParameter(program)

        return super().getNextInstructionPointer(program)


class AdjustRelativeBaseInst(OneParameterInst):
    def performComputation(self, program):
        shift = self.parameters[0].evaluateParameter(program)
        program.relative_base += shift


class QuitInst(IntcodeInstruction):
    def __init__(self):
        self.endComputations = True

    def extractParameters(self, program):
        return []

    def performComputation(self, program):
        pass