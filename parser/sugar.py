from parser.kernel import Sequence

def intersperse(parser, parsers):
    return Sequence([p for p in inter(parser, parsers)])

def inter(delimiter, iterable):
    it = iter(iterable)
    yield next(it)
    for p in it:
        yield delimiter
        yield p