import pytest

from rusty_iterators import LIter


def test_next_returns_next_element() -> None:
    it = LIter.from_items(1, 2, 3)

    assert it.next() == 1
    assert it.next() == 2
    assert it.next() == 3


def test_next_on_empty_iterator() -> None:
    it = LIter.from_items()

    with pytest.raises(StopIteration):
        it.next()


def test_collect_returns_original_items() -> None:
    assert LIter.from_items(1, 2, 3).collect() == [1, 2, 3]


def test_collect_into() -> None:
    assert LIter.from_items(1, 2, 3).collect_into(tuple) == (1, 2, 3)
    assert LIter.from_items(1, 2, 3).collect_into(list) == [1, 2, 3]
    assert LIter.from_items(1, 2, 3).collect_into(set) == {1, 2, 3}
    assert LIter.from_items(1, 2, 3).collect_into(frozenset) == {1, 2, 3}
