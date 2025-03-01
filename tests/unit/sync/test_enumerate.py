from rusty_iterators import LIter


def test_enumerate_iterator() -> None:
    it = LIter.from_items("a", "b", "c").enumerate()

    assert it.collect() == [(0, "a"), (1, "b"), (2, "c")]


def test_enumerate_empty_iterator() -> None:
    assert LIter.from_items().enumerate().collect() == []


def test_enumerate_copy() -> None:
    it = LIter.from_items(1, 2, 3).enumerate()
    it.next()

    cp = it.copy()

    assert it.collect() == cp.collect() == [(1, 2), (2, 3)]
