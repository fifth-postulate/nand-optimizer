from parser.parser import Any, Map, Sequence, Word

def assert_unique_parse(parses, expected_result, expected_rest):
    assert len(parses) == 1
    (result, rest) = parses[0]
    assert result == expected_result
    assert rest == expected_rest

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