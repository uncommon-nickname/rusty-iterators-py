import pytest

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


def test_iter_iterator_cannot_be_copied() -> None:
    it = LIter.from_it(iter(range(10)))

    assert not it.can_be_copied()

    with pytest.raises(Exception):
        it.copy()


def test_items_iterator_can_be_copied() -> None:
    it = LIter.from_items(1, 2, 3)
    it.next()

    assert it.can_be_copied()

    cp = it.copy()

    assert it.collect() == cp.collect() == [2, 3]
