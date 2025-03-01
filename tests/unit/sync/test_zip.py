import pytest

from rusty_iterators import LIter


def test_zip_returns_paired_items() -> None:
    it = LIter.from_items(1, 2).zip(LIter.from_items("a", "b"))

    assert it.next() == (1, "a")
    assert it.next() == (2, "b")


def test_zip_returns_shorter_iterator_length() -> None:
    it = LIter.from_items(1, 2, 3).zip(LIter.from_items("a", "b"))

    assert it.collect() == [(1, "a"), (2, "b")]


def test_empty_zip() -> None:
    it = LIter.from_items().zip(LIter.from_items("a", "b"))

    with pytest.raises(StopIteration):
        it.next()


def test_zip_copy_saves_state_of_iterators() -> None:
    it = LIter.from_items(1, 2).zip(LIter.from_items("a", "b"))
    it.next()

    cp = it.copy()

    assert cp.collect() == [(2, "b")]
    assert it.collect() == [(2, "b")]
