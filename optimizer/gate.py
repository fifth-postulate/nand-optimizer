from enum import Enum

class Gate:
    def __init__(self):
        pass

    def output(self):
        raise NotImplementedError('should be implemented by subclasses')

class High(Gate):
    def __init__(self):
        super().__init__()

    def output(self):
        return DigitalValue.HIGH

class Low(Gate):
    def __init__(self):
        super().__init__()

    def output(self):
        return DigitalValue.LOW

class Not(Gate):
    def __init__(self, gate):
        super().__init__()
        self.gate = gate

    def output(self):
        return self.gate.output().negate()

class Or(Gate):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def output(self):
        return self.left.output() + self.right.output()

class And(Gate):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def output(self):
        return self.left.output() * self.right.output()

class DigitalValue(Enum):
    HIGH = '1'
    LOW = '0'

    def negate(self):
        if self == DigitalValue.HIGH:
            return DigitalValue.LOW
        elif self == DigitalValue.LOW:
            return DigitalValue.HIGH
        else:
            raise ValueError(f'{repr(self)} is not a digital value?!')

    def __add__(self, other):
        if not isinstance(other, DigitalValue):
            raise ValueError(f'can only add digital value, found: {repr(other)}')
        
        if self == DigitalValue.LOW:
            return other
        else:
            return self

    def __mul__(self, other):
        if not isinstance(other, DigitalValue):
            raise ValueError(f'can only multiply digital value, found: {repr(other)}')
        
        if self == DigitalValue.LOW:
            return self
        else:
            return other


    def __str__(self):
        return self.value

    @staticmethod
    def from_string(representation):
        for candidate in DigitalValue:
            if candidate.value == representation:
                return candidate
        raise ValueError(f'"{representation}" is not a digital value')
