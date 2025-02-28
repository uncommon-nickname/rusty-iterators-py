from rusty_iterators import LIter


def test_sequence_constructor() -> None:
    assert LIter.from_seq("ab").collect() == ["a", "b"]
    assert LIter.from_seq([1, 2, 3]).collect() == [1, 2, 3]


def test_iterator_constructor() -> None:
    assert LIter.from_it(iter(range(4))).collect() == [0, 1, 2, 3]


def test_items_constructor() -> None:
    assert LIter.from_items(1, 2, 3).collect() == [1, 2, 3]


def test_sequence_iterator_can_be_copied() -> None:
    it = LIter.from_seq("abcd")
    it.next()

    assert it.can_be_copied()

    cp = it.copy()

    assert it.collect() == cp.collect() == ["b", "c", "d"]


def test_iter_iterator_can_be_copied() -> None:
    it = LIter.from_it(x for x in [1, 2, 3, 4, 5])
    it.next()

    assert it.can_be_copied()

    cp1 = it.copy()
    cp1.next()

    cp2 = cp1.copy()
    cp2.next()

    assert it.collect() == [2, 3, 4, 5]
    assert cp1.collect() == [3, 4, 5]
    assert cp2.collect() == [4, 5]


def test_items_iterator_can_be_copied() -> None:
    it = LIter.from_items(1, 2, 3)
    it.next()

    assert it.can_be_copied()

    cp = it.copy()

    assert it.collect() == cp.collect() == [2, 3]
