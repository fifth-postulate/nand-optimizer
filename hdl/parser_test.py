import hdl.parser as hdl
from parser.kernel_test import assert_unique_parse, assert_longest_parse

def test_parser():
    parser = hdl.parser()

    parses = parser.parse("""/**
    this is a or gate of with 4.
    */CHIP or4
    {
        IN a, b, c, d
        OUT out

        PARTS:
        or (a=a, b=b, out=v0);
        or (a=c, b=d, out=v1);
        or (a=v0, b=v1, out=out);
     }""")

    assert len(parses) > 0
    assert parses[0] == (('or4', ((['a', 'b', 'c', 'd'], ['out']), [('or', [('a', 'a'), ('b','b'), ('out','v0')]), ('or', [('a', 'c'), ('b','d'), ('out','v1')]), ('or', [('a', 'v0'), ('b','v1'), ('out','out')])])), '')

def test_non_comment_on_larger_example():
    parser = hdl.non_comment()

    parses = parser.parse("""/*
    this is a or gate of with 4.
    */CHIP or4
    {
        IN a, b, c, d
        OUT out

        PARTS:
        or (a=a, b=b, out=v0);
        or (a=c, b=d, out=v1);
        or (a=v0, b=v1, out=out);
     }""")

    assert len(parses) > 0
    assert parses[0] == ("""CHIP or4
    {
        IN a, b, c, d
        OUT out

        PARTS:
        or (a=a, b=b, out=v0);
        or (a=c, b=d, out=v1);
        or (a=v0, b=v1, out=out);
     }""", '')

def test_non_comment():
    parser = hdl.non_comment()

    parses = parser.parse('/* This is a comment block */Hello, World!// This is a line comment')

    assert_longest_parse(parses, 'Hello, World!', '')

def test_line_comment():
    parser = hdl.line_comment()

    parses = parser.parse('// This should be removed\n')

    assert_longest_parse(parses, '', '')

def test_block_comment():
    parser = hdl.block_comment()
    
    parses = parser.parse("""/*
    this is a comment block
    that is correctly parsed
    */""")

    assert_longest_parse(parses, '', '')

