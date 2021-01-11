from parser.parser import Any, Map, Predicate, Sequence, Word, complete, many

def parser():
    return complete(Map(lambda result: (result[2], result[4]), Sequence([
        keyword('CHIP'),
        whitespace(),
        name(),
        whitespace(),
        body()
    ])))

def keyword(word):
    return Word(word)

def whitespace():
    return ignore(many(Any([
        Word(' '),
        Word('\t'),
        Word('\n'),
    ])))

def ignore(parser):
    return Map(lambda _: '', parser)

def name():
    return Map(lambda result: ''.join([result[0]] + result[1]), Sequence([
        alpha(),
        many(alphanumeric()),
    ]))

def alpha():
    return Predicate(lambda character: character.isalpha())

def alphanumeric():
    return Predicate(lambda character: character.isalnum())

def body():
    return Map(lambda result: (result[2], result[4]), Sequence([
        Word('{'),
        whitespace(),
        pins(),
        whitespace(),
        implementation(),
        whitespace(),
        Word('}')
    ]))

def pins():
    return Map(lambda result: (result[0], result[1]), Sequence([
        input_pins(),
        output_pins()
    ]))

def input_pins():
    return pins_definition('IN')

def output_pins():
    return pins_definition('OUT')

def pins_definition(category):
    return Map(lambda result: [result[2]] + result[3], Sequence([
        Word(category),
        whitespace(),
        pin(),
        many(Map(lambda df: df[3], Sequence([
            whitespace(),
            comma(),
            whitespace(),
            pin(),
        ]))),
        whitespace(),
    ]))

def pin():
    return name()

def comma():
    return Word(',')

def implementation():
    return Map(lambda result: result[2], Sequence([
        Word('PARTS:'),
        whitespace(),
        many(internal_chip_part()),
    ]))

def internal_chip_part():
    return Map(lambda result: (result[0], result[4]), Sequence([
        name(),
        whitespace(),
        Word('('),
        whitespace(),
        connections(),
        whitespace(),
        Word(')'),
        whitespace(),
        Word(';'),
        whitespace(),
    ]))

def connections():
    return Map(lambda result: [result[0]] + result[1], Sequence([
        connection(),
        many(Map(lambda cs: cs[3], Sequence([
            whitespace(),
            comma(),
            whitespace(),
            connection(),
        ])))
    ]))

def connection():
    return Map(lambda result: (result[0], result[4]), Sequence([
        name(),
        whitespace(),
        Word('='),
        whitespace(),
        name(),
    ]))