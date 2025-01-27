import pytest

from rusty_iterators.core import RustyIter


def test_collected_values_are_filtered() -> None:
    it = RustyIter.from_items(1, 2, 3).filter(lambda x: x % 2 != 0)

    assert it.collect() == [1, 3]


def test_next_returns_first_that_fits() -> None:
    it = RustyIter.from_items(1, 2, 3).filter(lambda x: x % 2 != 0)

    assert it.next() == 1
    assert it.next() == 3


def test_next_on_empty_filter() -> None:
    it = RustyIter.from_items().filter(lambda x: x % 2 != 0)  # type: ignore[var-annotated]

    with pytest.raises(StopIteration):
        it.next()
