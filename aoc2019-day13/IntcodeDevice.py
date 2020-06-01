class IntcodeDevice():
    label = None

    def __init__(self, label='Device'):
        self.label = label

    def read(self):
        raise Exception(f'Read operation not defined for {self.label} device!!')

    def write(self, data):
        raise Exception(f'Write operation not defined for {self.label} device!!')

class ConsoleDevice(IntcodeDevice):

    def read(self):
        n = input(f'[{self.label}] Solicitando dato de entrada:')

        # Mmm.. there seems to be no standard way to check if some value is int... I found several ways
        # but people always point out flaws. So...
        try:
            data = int(n)
        except ValueError:
            raise Exception(f'[{self.label}] read [{n}] that is not an int!!')

        return data

    def write(self, data):
        print(f'>>>[{self.label}] OUTPUT: {data}')
