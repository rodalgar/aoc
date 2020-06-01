from IntcodeInstruction import AdditionInst, MultiplyInst, LessThanInst, EqualsInst, InputInst, OutputInst, \
    JumpIfTrueInst, JumpIfFalseInst, AdjustRelativeBaseInst, QuitInst


class IntcodeProgram():
    MAX_SIZE_IMAGE = 5000
    IP = None
    code = None
    relative_base = None

    def __init__(self, code, relative_base=0):
        self.IP = 0
        self.relative_base = relative_base
        self.code = self.__expand_code(code)  # maybe code.copy() ?

    def __expand_code(self, code):
        assert len(code) < IntcodeProgram.MAX_SIZE_IMAGE, \
            f'Program is too big! program size {len(code)}. Max size {IntcodeProgram.MAX_SIZE_IMAGE}'
        return code + ((IntcodeProgram.MAX_SIZE_IMAGE - len(code)) * [0])


class IntcodeInterpreterV5():
    instructions = None
    program = None

    def __init__(self):
        self.instructions = {}
        # TODO: Inject instruction set
        # Arithmetic
        self.instructions[1] = AdditionInst()
        self.instructions[2] = MultiplyInst()

        # IO
        self.instructions[3] = InputInst()
        self.instructions[4] = OutputInst()

        # Logic
        self.instructions[7] = LessThanInst()
        self.instructions[8] = EqualsInst()

        # Jump
        self.instructions[5] = JumpIfTrueInst()
        self.instructions[6] = JumpIfFalseInst()

        # Mem
        self.instructions[9] = AdjustRelativeBaseInst()

        # STOP
        self.instructions[99] = QuitInst()

    def __getNextInstructionType(self, program):
        opcode = program.code[program.IP]
        return opcode % 100

    def getInstruction(self, program):
        opcode = self.__getNextInstructionType(program)
        if opcode in self.instructions:
            instruction = self.instructions[opcode]
            return instruction
        else:
            raise Exception(
                'UNKNOWN opcode {} ({}) at position {}.\nPROGRAM: {}'.format(opcode, program.code[program.IP],
                                                                             program.IP, program.code))
        return None

    def __loadProgram(self, ext_program):
        self.program = IntcodeProgram(ext_program)

    def compute(self, ext_program):
        self.__loadProgram(ext_program)

        while True:
            isLastStep = self.nextStep()
            if isLastStep:
                break

        return self.program.code

    def beginStep(self, ext_program):
        self.__loadProgram(ext_program)

    def nextStep(self):
        assert self.program is not None, 'There is no program loaded!'
        # Extract next instruction
        instruction = self.getInstruction(self.program)

        if instruction.mustEndComputations():
            return True
        else:
            # Otherwise, compute instruction
            instruction.compute(self.program)
            # Change IP (Instruction Pointer)
            self.program.IP = instruction.getNextInstructionPointer(self.program)

        return False

    def getNextInstructionType(self):
        assert self.program is not None, 'There is no program loaded!'

        return self.__getNextInstructionType(self.program)