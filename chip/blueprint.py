import chip.error as error

class Builder:
    def __init__(self):
        pass

    def build(self):
        return []

class Nand:
    def build(self):
        inputs = {'a': Bus(1), 'b': Bus(1) }
        outputs = {'out': Bus(1) }
        tree = Tree(inputs['a'], inputs['b'], outputs['out'])
        return Chip('nand', inputs, outputs, tree)

class Not:
    def build(self):
        inputs = {'a': Bus(1) }
        outputs = {'out': Bus(1) }
        tree = Tree(inputs['a'], inputs['a'], outputs['out'])
        return Chip('not', inputs, outputs, tree)

class And:
    def build(self):
        inputs = {'a': Bus(1), 'b': Bus(1)}
        outputs = {'out': Bus(1) }
        intermediates = {'v': Tree(inputs['a'], inputs['b'], Bus(1))}
        tree = Tree(intermediates['v'], intermediates['v'], outputs['out'])
        return Chip('not', inputs, outputs, tree)


class Chip:
    def  __init__(self, name, inputs, outputs, tree):
        self.name = name 
        self.input = inputs
        self.output = outputs
        self.tree = tree

    def set(self, name, value):
        if name in self.input:
            self.input[name].set(value)
            self.update()
        else:
            raise error.NotAnInput(name, self.name)

    def update(self):
        self.tree.update()

    def get(self, name):
        if name in self.output:
            return self.output[name].get()
        else:
            raise error.NotAnOutput(name, self.name)

class Tree:
    def __init__(self, a, b, out):
        self.a = a
        self.b = b
        self.out = out

    def update(self):
        self.a.update()
        self.b.update()
        if not (self.a.get() == 1 and self.b.get() == 1):
            self.out.set(1)
        else:
            self.out.set(0)

    def get(self):
        return self.out.get()

class Bus:
    def __init__(self, width):
        self.width = width
        self.modulus = 2**width
        self.value = 0

    def set(self, value):
        self.value = value % self.modulus

    def update(self):
        pass

    def get(self):
        return self.value