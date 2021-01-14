from parser.kernel import Any, Filter, Map, Predicate, Sequence, Success, Word, atleast, many
from parser.sugar import intersperse
from tests.kernel_test import assert_unique_parse

def test_intersperse():
    parser = intersperse(Word(','), [Word('A'), Word('B'), Word('C')])

    parses = parser.parse('A,B,C')

    assert_unique_parse(parses, ['A', ',', 'B', ',', 'C'], '')

