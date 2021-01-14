from parser.kernel import Any, Avoid, Chain, Lazy, Map, Predicate, Producing, Sequence, Word, complete, many, optionally
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
        Word('{'),
        pins(),
        implementation(),
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
    return Map(lambda result: (result[0], result[4]), intersperse(whitespace(), [
        name(),
        Word('='),
        name(),
    ]))

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
