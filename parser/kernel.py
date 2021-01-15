class Parser:
    def __init__(self):
        pass
    
    def parse(self, record):
        raise NotImplementedError('the parse method should be implemented by subclasses')

class Success(Parser):
    def __init__(self):
        super().__init__()

    def parse(self, record):
        return [('', record)]

class Predicate(Parser):
    def __init__(self, predicate):
        super().__init__()
        self.predicate = predicate

    def parse(self, record):
        if len(record) > 0 and self.predicate(record[0]):
            return [(record[0], record[1:])]
        else:
            return []

class Word(Parser):
    def __init__(self, word):
        super().__init__()
        self.word = word

    def parse(self, record):
        if record.startswith(self.word):
            return [(self.word[:], record[len(self.word):])]
        else:
            return []

class Any(Parser):
    def __init__(self, parsers):
        super().__init__()
        self.parsers = parsers

    def parse(self, record):
        return [(result, rest) for parser in self.parsers for (result, rest) in parser.parse(record)]

class Sequence(Parser):
    def __init__(self, parsers):
        super().__init__()
        self.parsers = parsers

    def parse(self, record):
        return parse_sequence(self.parsers, record)

def parse_sequence(parsers, record):
    if not parsers:
        return [([], record)]
    else:
        parser = parsers[0]
        return [([intermediate_result] + result, rest) for (intermediate_result, intermediate_rest) in parser.parse(record) for (result, rest) in parse_sequence(parsers[1:], intermediate_rest)]

class Map(Parser):
    def __init__(self, transform, parser):
        super().__init__()
        self.parser = parser
        self.transform = transform

    def parse(self, record):
        return [(self.transform(result), rest) for (result, rest) in self.parser.parse(record)]

class Lazy(Parser):
    def __init__(self, parser_producer):
        super().__init__()
        self.parser_producer = parser_producer

    def parse(self, record):
        parser = self.parser_producer()
        return parser.parse(record)

class Filter(Parser):
    def __init__(self, predicate, parser):
        super().__init__()
        self.predicate = predicate
        self.parser = parser

    def parse(self, record):
        return [(result, rest) for (result, rest) in self.parser.parse(record) if self.predicate((result, rest))]

class Avoid(Parser):
    def __init__(self, word):
        super().__init__()
        self.word = word

    def parse(self, record):
        index = 0
        while index < len(record) and not record[index:].startswith(self.word):
            index += 1
        return [(record[0:index], record[index:])]

class Chain(Parser):
    def __init__(self, first, second):
        super().__init__()
        self.first = first
        self.second = second

    def parse(self, record):
        return [(result, second_rest + first_rest) for (intermediate, first_rest) in self.first.parse(record) for (result, second_rest) in self.second.parse(intermediate)]

class Producing(Parser):
    def __init__(self, parser):
        super().__init__()
        self.parser = parser

    def parse(self, record):
        return [(result, rest) for (result, rest) in self.parser.parse(record) if not rest == record]

def complete(parser):
    return Filter(lambda pair: pair[1] == '', parser)

def many(parser):
    return Many(parser) 
    # Below would be the combinatorial implementation. Unfortunately this easily blows the stack due to recursion. Therefore, we have chosen to implement that by hand. 
    # return Any([
    #     Map(lambda result: [result[0]] + result[1], Sequence([parser, Lazy(lambda : many(parser))])),
    #     Map(lambda result: [], Success()),
    # ])

class Many(Parser):
    def __init__(self, parser):
        super().__init__()
        self. parser = parser

    def parse(self, record):
        accumulator = [([], record)]
        last = accumulator
        while True:
            new = [(prefix + [result], rest) for (prefix, remaining) in last for (result, rest) in self.parser.parse(remaining)]
            accumulator.extend(new)
            last = new
            if len(new) == 0:
                break
        parses = sorted(accumulator, key=lambda p: len(p[1]))
        return parses

def atleast(number, parser):
    return Filter(lambda pair: len(pair[0]) >= number, many(parser))

def optionally(parser):
    return Any([
        parser,
        Success(),
    ])