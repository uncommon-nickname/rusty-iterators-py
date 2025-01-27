import pytest

from rusty_iterators.core import RustyIter


def test_next_returns_next_element() -> None:
    it = RustyIter.from_items(1, 2, 3)

    assert it.next() == 1
    assert it.next() == 2
    assert it.next() == 3


def test_next_on_empty_iterator() -> None:
    it = RustyIter.from_items()  # type: ignore[var-annotated]

    with pytest.raises(StopIteration):
        it.next()


def test_collect_returns_original_items() -> None:
    it = RustyIter.from_items(1, 2, 3)

    assert it.collect() == [1, 2, 3]
