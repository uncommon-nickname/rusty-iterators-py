from rusty_iterators import LIter


def test_multiple_chains() -> None:
    it = LIter.from_items(1, 2).chain(LIter.from_items(3, 4)).chain(LIter.from_items(5, 6))

    assert it.collect() == [1, 2, 3, 4, 5, 6]


def test_chain_can_be_copied() -> None:
    it = LIter.from_items(1, 2).chain(LIter.from_items(3, 4))
    it.next()

    assert it.can_be_copied()

    cp = it.copy()

    assert it.collect() == cp.collect() == [2, 3, 4]
