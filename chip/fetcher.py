import os
import hdl.parser as hdl 
import chip.error as error
from chip.blueprint import Builder

class FileFetcher:
    def __init__(self, directory):
        self.directory = directory
        self.parser = hdl.parser()

    def fetch(self, name):
        source = os.path.join(self.directory, f'{name}.hdl')
        if os.path.exists(source):
            with open(source, 'r') as file:
                definition = file.read()
                parses = self.parser.parse(definition)
                if len(parses) > 0:
                    return parses[0][0]
                else:
                    raise error.CouldNotParseChip()
        else:
            raise error.NonExistingChip()
