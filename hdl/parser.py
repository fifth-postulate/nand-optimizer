from parser.kernel import Any, Avoid, Chain, Lazy, Map, Predicate, Producing, Sequence, Word, atleast, complete, many, optionally
from parser.sugar import intersperse

def parser():
    return Chain(non_comment(), chip())

def chip():
    return complete(Map(lambda result: (result[2], result[4]), intersperse(whitespace(), [
        keyword('CHIP'),
        name(),
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
    return Map(lambda result: (result[2], result[4]), intersperse(whitespace(), [
        bracket('{'),
        interface(),
        implementation(),
        bracket('}')
    ]))

def bracket(form):
    return Word(form)

def interface():
    return Map(lambda result: (result[0], result[1]), Sequence([
        input_definitions(),
        output_definitions()
    ]))

def input_definitions():
    return interface_definitions('IN')

def output_definitions():
    return interface_definitions('OUT')

def interface_definitions(category):
    return Map(lambda result: [result[2]] + result[3], Sequence([
        keyword(category),
        whitespace(),
        interface_definition(),
        many(Map(lambda df: df[3], Sequence([
            whitespace(),
            comma(),
            whitespace(),
            interface_definition(),
        ]))),
        whitespace(),
        colon(),
        whitespace(),
    ]))

def interface_definition():
    return Any([
        bus(),
        pin(),
    ])

def bus():
    return Map(lambda result: (result[0], result[2]), Sequence([
        name(),
        bracket('['),
        number(),
        bracket(']')
    ]))

def number():
    return Map(lambda result: int(''.join(result)), atleast(1, digit()))

def digit():
    return Predicate(lambda character: character.isdigit())

def pin():
    return Map(lambda id: (id, 1), name())

def comma():
    return Word(',')

def colon():
    return Word(';')

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
        bracket('('),
        whitespace(),
        connections(),
        whitespace(),
        bracket(')'),
        whitespace(),
        colon(),
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
    return Map(lambda result: (result[0], result[4]), intersperse(whitespace(), [
        name(),
        assignment(),
        name(),
    ]))

def assignment():
    return Word('=')

def non_comment():
    return Map(lambda result: ''.join(result), complete(many(Any([
        block_comment(),
        line_comment(),
        any_character(),
    ]))))

def block_comment():
    return ignore(Sequence([
        Word('/*'),
        optionally(many(Any([
            Lazy(block_comment),
            Producing(Avoid('*/'))
        ]))),
        Word('*/'),
    ]))

def line_comment():
    return ignore(Sequence([
        Word('//'),
        many(not_newline()),
        optionally(newline()),       
    ]))

def not_newline():
    return Predicate(lambda character: not character == '\n')

def newline():
    return Predicate(lambda character: character == '\n')

def any_character():
    return Predicate(lambda _: True)
