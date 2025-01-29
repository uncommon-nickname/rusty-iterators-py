import pytest

from rusty_iterators.lib import LIter


def test_collected_values_have_callable_applied() -> None:
    it = LIter.from_items(1, 2, 3).map(lambda x: x * 2)

    assert it.collect() == [2, 4, 6]


def test_next_applies_callable() -> None:
    it = LIter.from_items(1, 2, 3).map(lambda x: str(x))

    assert it.next() == "1"
    assert it.next() == "2"
    assert it.next() == "3"


def test_next_on_empty_map() -> None:
    it = LIter.from_items().map(lambda x: x * 2)  # type: ignore[var-annotated]

    with pytest.raises(StopIteration):
        it.next()
