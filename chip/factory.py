import os
from chip.fetcher import FileFetcher
from chip.blueprint import Builder

class Factory:
    def __init__(self, buildins = { 'nand': Builder() }, fetcher = FileFetcher(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'definitions')))):
        self.buildins = buildins
        self.fetcher = fetcher
        self.cache = {}

    def chip(self, name):
        if name in self.buildins:
            return self.buildins[name]
        elif name in self.cache:
            return self.cache[name]
        else:
            blueprint = self.fetcher.fetch(name)
            self.cache[name] = blueprint
            return blueprint
