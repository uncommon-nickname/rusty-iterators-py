import pytest

from rusty_iterators import LIter


def test_collected_values_are_filtered() -> None:
    it = LIter.from_items(1, 2, 3).filter(lambda x: x % 2 != 0)

    assert it.collect() == [1, 3]


def test_next_returns_first_that_fits() -> None:
    it = LIter.from_items(1, 2, 3).filter(lambda x: x % 2 != 0)

    assert it.next() == 1
    assert it.next() == 3


def test_next_on_empty_filter() -> None:
    it = LIter.from_items().filter(lambda x: x % 2 != 0)

    with pytest.raises(StopIteration):
        it.next()


def test_filter_iterator_can_be_copied() -> None:
    it = LIter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0)
    it.next()

    assert it.can_be_copied()

    cp = it.copy()

    assert it.collect() == cp.collect() == [4]
