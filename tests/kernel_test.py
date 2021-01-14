from parser.kernel import Any, Avoid, Chain, Filter, Map, Predicate, Sequence, Success, Word, atleast, many, optionally

def assert_unique_parse(parses, expected_result, expected_rest):
    assert len(parses) == 1
    (result, rest) = parses[0]
    assert result == expected_result
    assert rest == expected_rest

def assert_longest_parse(parses, expected_result, expected_rest):
    assert len(parses) > 0
    (result, rest) = parses[0]
    assert result == expected_result
    assert rest == rest

def assert_failed(parses):
    assert not parses

def test_success():
    parser = Success()

    parses = parser.parse('Test')

    assert_unique_parse(parses, '', 'Test')

def test_predicate():
    parser = Predicate(lambda character: character.isdigit())

    parses = parser.parse('3435')

    assert_unique_parse(parses, '3', '435')

def test_predicate_with_empty_string():
    parser = Predicate(lambda character: character.isdigit())

    parses = parser.parse('')

    assert_failed(parses)

def test_word():
    parser = Word('Hello')

    parses = parser.parse('Hello, World!')

    assert_unique_parse(parses, 'Hello', ', World!')

def test_any():
    parser = Any([
        Word('A'),
        Word('B'),
    ])

    parses = parser.parse('AB')

    assert_unique_parse(parses, 'A', 'B')

def test_sequence():
    parser = Sequence([
        Word('A'),
        Word('B'),
    ])

    parses = parser.parse('AB')

    assert_unique_parse(parses, ['A', 'B'], '')

def test_map():
    parser = Map(lambda result: ''.join(result), Sequence([
        Word('A'),
        Word('B'),
    ]))

    parses = parser.parse('ABC')

    assert_unique_parse(parses, 'AB', 'C')

def test_filter():
    parser = Filter(lambda out: out[0].isupper(), Word('A'))

    parses = parser.parse('A')
    
    assert_unique_parse(parses, 'A', '')

def test_avoid():
    parser = Avoid('A!')

    parses = parser.parse('BBBBBBBBBA!')

    assert_unique_parse(parses, 'BBBBBBBBB', 'A!')

def test_avoid_when_failing():
    parser = Avoid('A!')

    parses = parser.parse('A!')

    assert_unique_parse(parses, '', 'A!')

def test_chain():
    parser = Chain(Word('ABC'), Word('A'))

    parses = parser.parse('ABCD')

    assert_unique_parse(parses, 'A', 'BCD')

def test_many():
    parser = many(Word('A'))

    parses = parser.parse('AAA')

    assert len(parses) == 4 
    assert parses[0] == (['A', 'A', 'A'], '')
    assert parses[1] == (['A', 'A'], 'A')
    assert parses[2] == (['A'], 'AA')
    assert parses[3] == ([], 'AAA')

def test_atleast():
    parser = atleast(2, Word('A'))

    parses = parser.parse('AAA')

    assert len(parses) == 2 
    assert parses[0] == (['A', 'A', 'A'], '')
    assert parses[1] == (['A', 'A'], 'A')

def test_optionally():
    parser = optionally(Word('A'))

    parses = parser.parse('A')

    assert len(parses) == 2 
    assert parses[0] == ('A', '')
    assert parses[1] == ('', 'A')
