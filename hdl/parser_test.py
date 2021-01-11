import hdl.parser as hdl

def test_parser():
    parser = hdl.parser()

    parses = parser.parse("""CHIP or4
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
