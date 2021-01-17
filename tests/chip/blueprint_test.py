from chip.blueprint import And, Nand, Not

def test_nand_builder():
    chip = Nand().build()

    chip.set('a', 0)
    chip.set('b', 0)
    assert chip.get('out') == 1

    chip.set('a', 1)
    chip.set('b', 0)
    assert chip.get('out') == 1

    chip.set('a', 0)
    chip.set('b', 1)
    assert chip.get('out') == 1

    chip.set('a', 1)
    chip.set('b', 1)
    assert chip.get('out') == 0

def test_not_builder():
    chip = Not().build()

    chip.set('a', 0)
    assert chip.get('out') == 1

    chip.set('a', 1)
    assert chip.get('out') == 0

def test_and_builder():
    chip = And().build()

    chip.set('a', 0)
    chip.set('b', 0)
    assert chip.get('out') == 0

    chip.set('a', 1)
    chip.set('b', 0)
    assert chip.get('out') == 0

    chip.set('a', 0)
    chip.set('b', 1)
    assert chip.get('out') == 0

    chip.set('a', 1)
    chip.set('b', 1)
    assert chip.get('out') == 1
