class ChipError(Exception):
    pass

class NonExistingChip(ChipError):
    pass

class CouldNotParseChip(ChipError):
    pass

class NotAnInput(ChipError):
    def __init__(self, input_name, chip_name):
        super().__init__(f'"{input_name}" is not an input in "{chip_name}"')

class NotAnOutput(ChipError):
    def __init__(self, output_name, chip_name):
        super().__init__(f'"{output_name}" is not an output in "{chip_name}"')